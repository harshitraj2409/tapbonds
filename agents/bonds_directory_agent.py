import os
import sys
import pandas as pd
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class BondsDirectoryAgent(BaseAgent):
    """
    Agent for handling queries related to the bonds directory
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the bonds directory agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        super().__init__(llm_handler, data_loader)
        self.system_message = """
        You are a specialized agent for the Bonds Directory on the Tap Bonds platform. Your role is to provide accurate information about bonds, including ISIN-level details, issuer information, credit ratings, maturity dates, and more.
        
        You have access to a comprehensive database of bonds and can answer queries about:
        - Specific bonds by ISIN
        - Bonds issued by a particular company
        - Bonds with specific characteristics (coupon rate, maturity date, credit rating, etc.)
        - Security details of bonds
        - Debenture trustees
        - Listing exchanges and trading status
        - Face values and other bond parameters
        
        Always provide accurate, up-to-date information and format your responses in a clear, structured manner.
        """
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "bonds_directory"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Agent for handling queries related to the bonds directory, including ISIN lookups, issuer information, and bond details."
    
    def process_query(self, query):
        """
        Process a user query related to the bonds directory
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Check if the query is about a specific ISIN
        isin_pattern = r'(?i)(?:ISIN\s*)?([A-Z]{2}[A-Z0-9]{10})'
        isin_match = re.search(isin_pattern, query)
        
        if isin_match:
            isin = isin_match.group(1)
            return self._get_bond_details(isin)
        
        # Check if the query is about bonds issued by a company
        if any(phrase in query.lower() for phrase in ["issued by", "issuances done by", "bonds from", "bonds by"]):
            # Extract company name from query
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_bonds_by_issuer(company_name)
        
        # Check if the query is about filtering bonds
        if any(phrase in query.lower() for phrase in ["find me", "show me", "list", "filter"]):
            filters = self._extract_filters(query)
            if filters:
                return self._filter_bonds(filters)
        
        # Check if the query is about bonds maturing in a specific year
        year_pattern = r'(?i)maturing\s+in\s+(\d{4})'
        year_match = re.search(year_pattern, query)
        
        if year_match:
            year = year_match.group(1)
            return self._get_bonds_maturing_in_year(int(year))
        
        # If no specific pattern is matched, use the LLM to generate a response
        # First, enrich the query with relevant bond data
        enriched_query = self._enrich_query(query)
        
        # Then, use the LLM to generate a response
        return self.llm_handler.get_completion(enriched_query, self.system_message)
    
    def _get_bond_details(self, isin):
        """
        Get details for a specific bond by ISIN
        
        Args:
            isin (str): ISIN of the bond
        
        Returns:
            str: Bond details
        """
        bond_details = self.data_loader.get_bond_by_isin(isin)
        
        if bond_details is None or bond_details.empty:
            return f"I couldn't find any bond with ISIN {isin}. Please check the ISIN and try again."
        
        # Format bond details as a prompt for the LLM
        bond_details_str = f"Bond details for ISIN {isin}:\n\n"
        for column in bond_details.columns:
            bond_details_str += f"{column}: {bond_details[column].iloc[0]}\n"
        
        # Get cashflows for the bond
        cashflows = self.data_loader.get_cashflows_by_isin(isin)
        if cashflows is not None and not cashflows.empty:
            bond_details_str += f"\nCash flows for ISIN {isin}:\n\n"
            cashflows_df = cashflows[['cash_flow_date', 'cash_flow_amount', 'principal_amount', 'interest_amount']]
            bond_details_str += cashflows_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bond details, provide a comprehensive and well-formatted response to a user asking about ISIN {isin}:
        
        {bond_details_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include all key information such as:
        - Issuer Name (from company_name)
        - Type of Issuer (from issuer_details)
        - Sector (from issuer_details)
        - Coupon Rate (from coupon_details)
        - Instrument Name (from instrument_details)
        - Face Value (extract from relevant field)
        - Total Issue Size (from issue_size)
        - Redemption Date (from maturity_date)
        - Credit Rating (from credit_rating_details)
        - Listing Details (from listing_details)
        - Key Documents (from key_documents_details)
        
        If there are cash flows, summarize them in a table format.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_bonds_by_issuer(self, company_name):
        """
        Get bonds issued by a specific company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Bonds issued by the company
        """
        bonds = self.data_loader.get_bonds_by_issuer(company_name)
        
        if bonds is None or bonds.empty:
            return f"I couldn't find any bonds issued by {company_name}. Please check the company name and try again."
        
        # Format bonds as a prompt for the LLM
        bonds_str = f"Bonds issued by {company_name}:\n\n"
        
        # Select relevant columns
        relevant_columns = ['isin', 'maturity_date', 'issue_size']
        
        # Add coupon_details if available
        if 'coupon_details' in bonds.columns:
            relevant_columns.append('coupon_details')
        
        # Add credit_rating_details if available
        if 'credit_rating_details' in bonds.columns:
            relevant_columns.append('credit_rating_details')
        
        bonds_df = bonds[relevant_columns]
        bonds_str += bonds_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds issued by {company_name}:
        
        {bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the number of bonds issued, how many are active vs. matured, and a table of the bonds with key details.
        
        For each bond, try to extract and present:
        - ISIN
        - Coupon Rate (from coupon_details)
        - Maturity Date
        - Face Value (if available)
        - Credit Rating (from credit_rating_details)
        - Issue Size
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _extract_company_name(self, query):
        """
        Extract company name from a query
        
        Args:
            query (str): User query
        
        Returns:
            str: Extracted company name
        """
        # Use the LLM to extract the company name
        prompt = f"""
        Extract the company name from the following query:
        
        "{query}"
        
        Respond with just the company name, nothing else.
        """
        
        return self.llm_handler.get_completion(prompt, temperature=0.3)
    
    def _extract_filters(self, query):
        """
        Extract filters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted filters
        """
        # Use the LLM to extract filters
        system_message = """
        You are a filter extraction assistant. Your task is to extract filter criteria from a user query about bonds.
        
        Extract the following filters if present:
        - coupon_rate_min: Minimum coupon rate (as a float)
        - coupon_rate_max: Maximum coupon rate (as a float)
        - maturity_date_min: Minimum maturity date (as YYYY-MM-DD)
        - maturity_date_max: Maximum maturity date (as YYYY-MM-DD)
        - credit_rating: List of acceptable credit ratings
        - security_type: Type of security (e.g., 'Secured', 'Unsecured')
        - issuer_type: Type of issuer (e.g., 'PSU', 'Non-PSU')
        - sector: Sector of the issuer
        
        Respond with a JSON object containing the extracted filters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "coupon_rate_min": {"type": ["number", "null"]},
                "coupon_rate_max": {"type": ["number", "null"]},
                "maturity_date_min": {"type": ["string", "null"]},
                "maturity_date_max": {"type": ["string", "null"]},
                "credit_rating": {"type": ["array", "null"], "items": {"type": "string"}},
                "security_type": {"type": ["string", "null"]},
                "issuer_type": {"type": ["string", "null"]},
                "sector": {"type": ["string", "null"]}
            }
        }
        
        return self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
    
    def _filter_bonds(self, filters):
        """
        Filter bonds based on criteria
        
        Args:
            filters (dict): Filter criteria
        
        Returns:
            str: Filtered bonds
        """
        filtered_bonds = self.data_loader.filter_bonds(filters)
        
        if filtered_bonds is None or filtered_bonds.empty:
            return "I couldn't find any bonds matching your criteria. Please try with different filters."
        
        # Format filtered bonds as a prompt for the LLM
        filtered_bonds_str = f"Bonds matching your criteria:\n\n"
        
        # Select relevant columns
        relevant_columns = ['isin', 'company_name', 'maturity_date', 'issue_size']
        
        # Add coupon_details if available
        if 'coupon_details' in filtered_bonds.columns:
            relevant_columns.append('coupon_details')
        
        # Add credit_rating_details if available
        if 'credit_rating_details' in filtered_bonds.columns:
            relevant_columns.append('credit_rating_details')
        
        filtered_bonds_df = filtered_bonds[relevant_columns]
        filtered_bonds_str += filtered_bonds_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following filtered bonds data, provide a comprehensive and well-formatted response to a user's filter query:
        
        {filtered_bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the number of bonds found and a table of the bonds with key details.
        
        For each bond, try to extract and present:
        - ISIN
        - Issuer Name (from company_name)
        - Coupon Rate (from coupon_details)
        - Maturity Date
        - Face Value (if available)
        - Credit Rating (from credit_rating_details)
        - Issue Size
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_bonds_maturing_in_year(self, year):
        """
        Get bonds maturing in a specific year
        
        Args:
            year (int): Year of maturity
        
        Returns:
            str: Bonds maturing in the year
        """
        bonds = self.data_loader.get_bonds_maturing_in_year(year)
        
        if bonds is None or bonds.empty:
            return f"I couldn't find any bonds maturing in {year}. Please try a different year."
        
        # Format bonds as a prompt for the LLM
        bonds_str = f"Bonds maturing in {year}:\n\n"
        
        # Select relevant columns
        relevant_columns = ['isin', 'company_name', 'maturity_date', 'issue_size']
        
        # Add coupon_details if available
        if 'coupon_details' in bonds.columns:
            relevant_columns.append('coupon_details')
        
        # Add credit_rating_details if available
        if 'credit_rating_details' in bonds.columns:
            relevant_columns.append('credit_rating_details')
        
        bonds_df = bonds[relevant_columns]
        bonds_str += bonds_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds maturing in {year}:
        
        {bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the number of bonds maturing in {year} and a table of the bonds with key details.
        
        For each bond, try to extract and present:
        - ISIN
        - Issuer Name (from company_name)
        - Coupon Rate (from coupon_details)
        - Maturity Date
        - Face Value (if available)
        - Credit Rating (from credit_rating_details)
        - Issue Size
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _enrich_query(self, query):
        """
        Enrich a query with relevant bond data
        
        Args:
            query (str): User query
        
        Returns:
            str: Enriched query
        """
        # Try to extract ISIN from query
        isin_pattern = r'(?i)(?:ISIN\s*)?([A-Z]{2}[A-Z0-9]{10})'
        isin_match = re.search(isin_pattern, query)
        
        if isin_match:
            isin = isin_match.group(1)
            bond_details = self.data_loader.get_bond_by_isin(isin)
            
            if bond_details is not None and not bond_details.empty:
                # Format bond details as a string
                bond_details_str = f"Bond details for ISIN {isin}:\n\n"
                for column in bond_details.columns:
                    bond_details_str += f"{column}: {bond_details[column].iloc[0]}\n"
                
                # Get cashflows for the bond
                cashflows = self.data_loader.get_cashflows_by_isin(isin)
                if cashflows is not None and not cashflows.empty:
                    bond_details_str += f"\nCash flows for ISIN {isin}:\n\n"
                    cashflows_df = cashflows[['cash_flow_date', 'cash_flow_amount', 'principal_amount', 'interest_amount']]
                    bond_details_str += cashflows_df.to_string(index=False)
                
                # Enrich the query with bond details
                enriched_query = f"""
                User query: {query}
                
                {bond_details_str}
                
                Based on the above bond details, please provide a comprehensive response to the user query.
                """
                
                return enriched_query
        
        # Try to extract company name from query
        company_name = self._extract_company_name(query)
        
        if company_name:
            bonds = self.data_loader.get_bonds_by_issuer(company_name)
            
            if bonds is not None and not bonds.empty:
                # Format bonds as a string
                bonds_str = f"Bonds issued by {company_name}:\n\n"
                
                # Select relevant columns
                relevant_columns = ['isin', 'maturity_date', 'issue_size']
                
                # Add coupon_details if available
                if 'coupon_details' in bonds.columns:
                    relevant_columns.append('coupon_details')
                
                # Add credit_rating_details if available
                if 'credit_rating_details' in bonds.columns:
                    relevant_columns.append('credit_rating_details')
                
                bonds_df = bonds[relevant_columns]
                bonds_str += bonds_df.to_string(index=False)
                
                # Enrich the query with bonds data
                enriched_query = f"""
                User query: {query}
                
                {bonds_str}
                
                Based on the above bonds data, please provide a comprehensive response to the user query.
                """
                
                return enriched_query
        
        return query 