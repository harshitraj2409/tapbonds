import os
import sys
import pandas as pd
import re
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class CashflowMaturityAgent(BaseAgent):
    """
    Agent for handling queries related to bond cash flows and maturity schedules
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the cashflow maturity agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        super().__init__(llm_handler, data_loader)
        self.system_message = """
        You are a specialized agent for Cash Flow & Maturity analysis on the Tap Bonds platform. Your role is to provide accurate information about bond cash flows, maturity schedules, and payment timelines.
        
        You have access to detailed cash flow data and can answer queries about:
        - Cash flow schedules for specific bonds
        - Maturity dates and redemption details
        - Interest payment dates and amounts
        - Principal repayment schedules
        - Bonds maturing in specific time periods
        
        Always provide accurate, up-to-date information and format your responses in a clear, structured manner.
        """
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "cashflow_maturity"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Agent for handling queries related to bond cash flows, maturity schedules, and payment timelines."
    
    def process_query(self, query):
        """
        Process a user query related to cash flows and maturity
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Check if the query is about a cash flow schedule for a specific ISIN
        if "cash flow" in query.lower() or "cashflow" in query.lower() or "payment schedule" in query.lower():
            # Extract ISIN from query
            isin_pattern = r'(?i)(?:ISIN\s*)?([A-Z]{2}[A-Z0-9]{10})'
            isin_match = re.search(isin_pattern, query)
            
            if isin_match:
                isin = isin_match.group(1)
                return self._get_cashflow_schedule(isin)
        
        # Check if the query is about bonds maturing in a specific year
        year_pattern = r'(?i)maturing\s+in\s+(\d{4})'
        year_match = re.search(year_pattern, query)
        
        if year_match:
            year = year_match.group(1)
            return self._get_bonds_maturing_in_year(int(year))
        
        # Check if the query is about bonds maturing in a specific month and year
        month_year_pattern = r'(?i)maturing\s+in\s+([a-zA-Z]+)\s+(\d{4})'
        month_year_match = re.search(month_year_pattern, query)
        
        if month_year_match:
            month = month_year_match.group(1)
            year = month_year_match.group(2)
            return self._get_bonds_maturing_in_month_year(month, int(year))
        
        # Check if the query is about the next interest payment for a specific ISIN
        if "next interest payment" in query.lower() or "next coupon payment" in query.lower():
            # Extract ISIN from query
            isin_pattern = r'(?i)(?:ISIN\s*)?([A-Z]{2}[A-Z0-9]{10})'
            isin_match = re.search(isin_pattern, query)
            
            if isin_match:
                isin = isin_match.group(1)
                return self._get_next_interest_payment(isin)
        
        # If no specific pattern is matched, use the LLM to generate a response
        # First, enrich the query with relevant cash flow data
        enriched_query = self._enrich_query(query)
        
        # Then, use the LLM to generate a response
        return self.llm_handler.get_completion(enriched_query, self.system_message)
    
    def _get_cashflow_schedule(self, isin):
        """
        Get the cash flow schedule for a specific bond
        
        Args:
            isin (str): ISIN of the bond
        
        Returns:
            str: Cash flow schedule
        """
        # Get bond details
        bond_details = self.data_loader.get_bond_by_isin(isin)
        
        if bond_details is None or bond_details.empty:
            return f"I couldn't find any bond with ISIN {isin}. Please check the ISIN and try again."
        
        # Get cash flows
        cashflows = self.data_loader.get_cashflows_by_isin(isin)
        
        if cashflows is None or cashflows.empty:
            return f"I couldn't find any cash flow data for ISIN {isin}. This bond may not have detailed cash flow information available."
        
        # Format bond details and cash flows as a prompt for the LLM
        bond_details_str = f"Bond details for ISIN {isin}:\n\n"
        for column in bond_details.columns:
            bond_details_str += f"{column}: {bond_details[column].iloc[0]}\n"
        
        cashflows_str = f"\nCash flow schedule for ISIN {isin}:\n\n"
        
        # Sort cash flows by date
        cashflows = cashflows.sort_values(by='cash_flow_date')
        
        # Select relevant columns
        cashflow_columns = ['cash_flow_date', 'cash_flow_amount', 'principal_amount', 'interest_amount']
        cashflows_df = cashflows[cashflow_columns]
        
        cashflows_str += cashflows_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bond details and cash flow schedule, provide a comprehensive and well-formatted response to a user asking about the cash flow schedule for ISIN {isin}:
        
        {bond_details_str}
        
        {cashflows_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the bond details (issuer, coupon, maturity) and a table of the cash flow schedule.
        
        For the cash flow table, include:
        - Payment Date
        - Type (Interest Payment, Principal Repayment, or both)
        - Amount
        
        Also include any relevant information about the bond's payment frequency, next payment date, and total remaining payments.
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
        - Coupon Rate (from coupon_details if available)
        - Maturity Date
        - Issue Size
        - Credit Rating (from credit_rating_details if available)
        
        Also mention that the user can ask for more detailed information about any specific bond by providing its ISIN.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_bonds_maturing_in_month_year(self, month, year):
        """
        Get bonds maturing in a specific month and year
        
        Args:
            month (str): Month of maturity
            year (int): Year of maturity
        
        Returns:
            str: Bonds maturing in the month and year
        """
        # Convert month name to month number
        try:
            month_num = datetime.strptime(month, '%B').month
        except ValueError:
            try:
                month_num = datetime.strptime(month, '%b').month
            except ValueError:
                return f"I couldn't understand the month '{month}'. Please provide a valid month name."
        
        # Get bonds maturing in the year
        bonds = self.data_loader.get_bonds_maturing_in_year(year)
        
        if bonds is None or bonds.empty:
            return f"I couldn't find any bonds maturing in {month} {year}. Please try a different month and year."
        
        # Filter bonds by month
        month_str = f"{year}-{month_num:02d}"
        bonds_in_month = bonds[bonds['maturity_date'].str.startswith(month_str, na=False)]
        
        if bonds_in_month.empty:
            return f"I couldn't find any bonds maturing in {month} {year}. Please try a different month and year."
        
        # Format bonds as a prompt for the LLM
        bonds_str = f"Bonds maturing in {month} {year}:\n\n"
        
        # Select relevant columns
        relevant_columns = ['isin', 'company_name', 'maturity_date', 'issue_size']
        
        # Add coupon_details if available
        if 'coupon_details' in bonds_in_month.columns:
            relevant_columns.append('coupon_details')
        
        # Add credit_rating_details if available
        if 'credit_rating_details' in bonds_in_month.columns:
            relevant_columns.append('credit_rating_details')
        
        bonds_df = bonds_in_month[relevant_columns]
        bonds_str += bonds_df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds maturing in {month} {year}:
        
        {bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the number of bonds maturing in {month} {year} and a table of the bonds with key details.
        
        For each bond, try to extract and present:
        - ISIN
        - Issuer Name (from company_name)
        - Coupon Rate (from coupon_details if available)
        - Maturity Date
        - Issue Size
        - Credit Rating (from credit_rating_details if available)
        
        Also mention that the user can ask for more detailed information about any specific bond by providing its ISIN.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_next_interest_payment(self, isin):
        """
        Get the next interest payment for a specific bond
        
        Args:
            isin (str): ISIN of the bond
        
        Returns:
            str: Next interest payment details
        """
        # Get bond details
        bond_details = self.data_loader.get_bond_by_isin(isin)
        
        if bond_details is None or bond_details.empty:
            return f"I couldn't find any bond with ISIN {isin}. Please check the ISIN and try again."
        
        # Get cash flows
        cashflows = self.data_loader.get_cashflows_by_isin(isin)
        
        if cashflows is None or cashflows.empty:
            return f"I couldn't find any cash flow data for ISIN {isin}. This bond may not have detailed cash flow information available."
        
        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Filter future cash flows
        future_cashflows = cashflows[cashflows['cash_flow_date'] > current_date]
        
        if future_cashflows.empty:
            return f"There are no future interest payments for ISIN {isin}. The bond may have matured or all payments have been made."
        
        # Sort cash flows by date
        future_cashflows = future_cashflows.sort_values(by='cash_flow_date')
        
        # Get the next cash flow
        next_cashflow = future_cashflows.iloc[0]
        
        # Format bond details and next cash flow as a prompt for the LLM
        bond_details_str = f"Bond details for ISIN {isin}:\n\n"
        for column in bond_details.columns:
            bond_details_str += f"{column}: {bond_details[column].iloc[0]}\n"
        
        next_cashflow_str = f"\nNext cash flow for ISIN {isin}:\n\n"
        for column in next_cashflow.index:
            next_cashflow_str += f"{column}: {next_cashflow[column]}\n"
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bond details and next cash flow, provide a comprehensive and well-formatted response to a user asking about the next interest payment for ISIN {isin}:
        
        {bond_details_str}
        
        {next_cashflow_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the bond details (issuer, coupon, maturity) and details of the next interest payment.
        
        For the next interest payment, include:
        - Payment Date
        - Interest Amount
        - Record Date (if available)
        
        Also include any relevant information about the bond's payment frequency and total remaining payments.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _enrich_query(self, query):
        """
        Enrich a query with relevant cash flow data
        
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
            
            # Get bond details
            bond_details = self.data_loader.get_bond_by_isin(isin)
            
            if bond_details is not None and not bond_details.empty:
                # Format bond details as a string
                bond_details_str = f"Bond details for ISIN {isin}:\n\n"
                for column in bond_details.columns:
                    bond_details_str += f"{column}: {bond_details[column].iloc[0]}\n"
                
                # Get cash flows
                cashflows = self.data_loader.get_cashflows_by_isin(isin)
                
                if cashflows is not None and not cashflows.empty:
                    # Sort cash flows by date
                    cashflows = cashflows.sort_values(by='cash_flow_date')
                    
                    # Select relevant columns
                    cashflow_columns = ['cash_flow_date', 'cash_flow_amount', 'principal_amount', 'interest_amount']
                    cashflows_df = cashflows[cashflow_columns]
                    
                    cashflows_str = f"\nCash flow schedule for ISIN {isin}:\n\n"
                    cashflows_str += cashflows_df.to_string(index=False)
                    
                    # Enrich the query with bond details and cash flows
                    enriched_query = f"""
                    User query: {query}
                    
                    {bond_details_str}
                    
                    {cashflows_str}
                    
                    Based on the above bond details and cash flow schedule, please provide a comprehensive response to the user query.
                    """
                    
                    return enriched_query
                else:
                    # Enrich the query with bond details only
                    enriched_query = f"""
                    User query: {query}
                    
                    {bond_details_str}
                    
                    Based on the above bond details, please provide a comprehensive response to the user query.
                    Note that detailed cash flow information is not available for this bond.
                    """
                    
                    return enriched_query
        
        # Try to extract year from query
        year_pattern = r'(?i)(?:year|in)\s+(\d{4})'
        year_match = re.search(year_pattern, query)
        
        if year_match:
            year = int(year_match.group(1))
            
            # Get bonds maturing in the year
            bonds = self.data_loader.get_bonds_maturing_in_year(year)
            
            if bonds is not None and not bonds.empty:
                # Format bonds as a string
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
                
                # Enrich the query with bonds data
                enriched_query = f"""
                User query: {query}
                
                {bonds_str}
                
                Based on the above bonds data, please provide a comprehensive response to the user query.
                """
                
                return enriched_query
        
        return query 