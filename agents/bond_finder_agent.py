import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class BondFinderAgent(BaseAgent):
    """
    Agent for handling queries related to the bond finder
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the bond finder agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        super().__init__(llm_handler, data_loader)
        self.system_message = """
        You are a specialized agent for the Bond Finder on the Tap Bonds platform. Your role is to help users discover and compare bonds across different platforms, find the best yields, and make informed investment decisions.
        
        The Bond Finder aggregates bond listings from partner platforms like SMEST and FixedIncome, providing users with essential bond details, including issuer name, ISINs, credit rating, yield range, maturity date, and availability across platforms.
        
        You can help users:
        - Find bonds available on different platforms
        - Compare yields across platforms
        - Identify the best investment opportunities
        - Filter bonds based on various criteria (yield, rating, maturity, etc.)
        
        Always provide accurate, up-to-date information and format your responses in a clear, structured manner.
        """
        
        # Mock data for bond finder (in a real implementation, this would come from the data loader)
        self.platforms = ["SMEST", "FixedIncome"]
        self.available_bonds = self._create_mock_available_bonds()
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "bond_finder"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Agent for handling queries related to the bond finder, including comparing bonds across platforms and finding the best yields."
    
    def process_query(self, query):
        """
        Process a user query related to the bond finder
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Check if the query is about available bonds
        if any(phrase in query.lower() for phrase in ["available", "show me what", "list all", "what bonds"]):
            return self._get_available_bonds()
        
        # Check if the query is about bonds from a specific issuer
        if any(phrase in query.lower() for phrase in ["where can i buy", "available from", "bonds from"]):
            # Extract issuer name from query
            issuer_name = self._extract_issuer_name(query)
            if issuer_name:
                return self._get_bonds_by_issuer(issuer_name)
        
        # Check if the query is about bonds with a specific yield
        if any(phrase in query.lower() for phrase in ["yield of more than", "yield above", "yield higher than"]):
            # Extract yield from query
            min_yield = self._extract_yield(query)
            if min_yield is not None:
                return self._get_bonds_by_yield(min_yield)
        
        # Check if the query is about the best yield
        if any(phrase in query.lower() for phrase in ["best yield", "highest yield", "maximum yield"]):
            return self._get_best_yield(query)
        
        # Check if the query is about bonds with a specific rating
        if any(phrase in query.lower() for phrase in ["rating of", "rated", "with a rating"]):
            # Extract rating from query
            rating = self._extract_rating(query)
            if rating:
                return self._get_bonds_by_rating(rating)
        
        # If no specific pattern is matched, use the LLM to generate a response
        # First, enrich the query with relevant bond data
        enriched_query = self._enrich_query(query)
        
        # Then, use the LLM to generate a response
        return self.llm_handler.get_completion(enriched_query, self.system_message)
    
    def _create_mock_available_bonds(self):
        """
        Create mock data for available bonds
        
        Returns:
            list: List of available bonds
        """
        return [
            {
                "issuer": "Tata Capital",
                "rating": "AAA",
                "yield_range": "7.5%-8.0%",
                "maturity": "2028",
                "available_at": "SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Indiabulls Housing Finance",
                "rating": "AA",
                "yield_range": "9.2%-9.8%",
                "maturity": "2027",
                "available_at": "FixedIncome, SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Piramal Capital",
                "rating": "A",
                "yield_range": "9.5%-10.1%",
                "maturity": "2026",
                "available_at": "SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Shriram Finance",
                "rating": "AA",
                "yield_range": "9.3%-9.9%",
                "maturity": "2029",
                "available_at": "FixedIncome",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "L&T Finance",
                "rating": "AAA",
                "yield_range": "8.0%-8.5%",
                "maturity": "2030",
                "available_at": "SMEST, FixedIncome",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Edelweiss Finance",
                "rating": "AA-",
                "yield_range": "9.0%-9.5%",
                "maturity": "2028",
                "available_at": "FixedIncome",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "HDFC",
                "rating": "AAA",
                "yield_range": "7.8%-8.2%",
                "maturity": "2031",
                "available_at": "SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Muthoot Finance",
                "rating": "AA+",
                "yield_range": "8.5%-9.0%",
                "maturity": "2027",
                "available_at": "FixedIncome, SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Bajaj Finance",
                "rating": "AAA",
                "yield_range": "7.9%-8.4%",
                "maturity": "2029",
                "available_at": "SMEST",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            },
            {
                "issuer": "Aditya Birla Finance",
                "rating": "AAA",
                "yield_range": "8.1%-8.6%",
                "maturity": "2028",
                "available_at": "FixedIncome",
                "min_investment": "₹10,000",
                "face_value": "₹1,000"
            }
        ]
    
    def _get_available_bonds(self):
        """
        Get all available bonds
        
        Returns:
            str: Available bonds
        """
        # Format available bonds as a prompt for the LLM
        available_bonds_str = "Available bonds on the platform:\n\n"
        
        # Create a DataFrame from the available bonds
        df = pd.DataFrame(self.available_bonds)
        available_bonds_str += df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following available bonds data, provide a comprehensive and well-formatted response to a user asking about available bonds:
        
        {available_bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a summary of the number of bonds available on each platform and a table of the bonds with key details.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_bonds_by_issuer(self, issuer_name):
        """
        Get bonds from a specific issuer
        
        Args:
            issuer_name (str): Name of the issuer
        
        Returns:
            str: Bonds from the issuer
        """
        # Filter bonds by issuer
        issuer_bonds = [bond for bond in self.available_bonds if issuer_name.lower() in bond["issuer"].lower()]
        
        if not issuer_bonds:
            return f"I couldn't find any bonds from {issuer_name} available on our partner platforms. Please check the issuer name and try again."
        
        # Format issuer bonds as a prompt for the LLM
        issuer_bonds_str = f"Bonds from {issuer_name} available on our partner platforms:\n\n"
        
        # Create a DataFrame from the issuer bonds
        df = pd.DataFrame(issuer_bonds)
        issuer_bonds_str += df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds from {issuer_name}:
        
        {issuer_bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include information about which platforms offer these bonds and the yield ranges available.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _extract_issuer_name(self, query):
        """
        Extract issuer name from a query
        
        Args:
            query (str): User query
        
        Returns:
            str: Extracted issuer name
        """
        # Use the LLM to extract the issuer name
        prompt = f"""
        Extract the issuer name from the following query:
        
        "{query}"
        
        Respond with just the issuer name, nothing else.
        """
        
        return self.llm_handler.get_completion(prompt, temperature=0.3)
    
    def _extract_yield(self, query):
        """
        Extract yield from a query
        
        Args:
            query (str): User query
        
        Returns:
            float: Extracted yield
        """
        # Use the LLM to extract the yield
        prompt = f"""
        Extract the minimum yield percentage from the following query:
        
        "{query}"
        
        Respond with just the number (e.g., 9.5), nothing else.
        """
        
        yield_str = self.llm_handler.get_completion(prompt, temperature=0.3)
        
        try:
            return float(yield_str)
        except ValueError:
            return None
    
    def _get_bonds_by_yield(self, min_yield):
        """
        Get bonds with a yield above a minimum value
        
        Args:
            min_yield (float): Minimum yield
        
        Returns:
            str: Bonds with a yield above the minimum
        """
        # Filter bonds by yield
        high_yield_bonds = []
        
        for bond in self.available_bonds:
            # Extract the lower bound of the yield range
            yield_range = bond["yield_range"]
            lower_bound = float(yield_range.split("-")[0].strip("%"))
            
            if lower_bound >= min_yield:
                high_yield_bonds.append(bond)
        
        if not high_yield_bonds:
            return f"I couldn't find any bonds with a yield of {min_yield}% or higher. Please try with a lower yield."
        
        # Format high yield bonds as a prompt for the LLM
        high_yield_bonds_str = f"Bonds with a yield of {min_yield}% or higher:\n\n"
        
        # Create a DataFrame from the high yield bonds
        df = pd.DataFrame(high_yield_bonds)
        high_yield_bonds_str += df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds with a yield of {min_yield}% or higher:
        
        {high_yield_bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include information about which platforms offer these bonds and the yield ranges available.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_best_yield(self, query):
        """
        Get bonds with the best yield
        
        Args:
            query (str): User query
        
        Returns:
            str: Bonds with the best yield
        """
        # Extract the bond term from the query (e.g., "5-year bonds")
        term = None
        
        if "year" in query:
            # Use the LLM to extract the term
            prompt = f"""
            Extract the bond term (in years) from the following query:
            
            "{query}"
            
            Respond with just the number (e.g., 5), nothing else.
            """
            
            term_str = self.llm_handler.get_completion(prompt, temperature=0.3)
            
            try:
                term = int(term_str)
            except ValueError:
                term = None
        
        # Filter bonds by term if specified
        if term:
            target_maturity = str(2023 + term)  # Assuming current year is 2023
            filtered_bonds = [bond for bond in self.available_bonds if bond["maturity"] == target_maturity]
        else:
            filtered_bonds = self.available_bonds
        
        if not filtered_bonds:
            return f"I couldn't find any bonds matching your criteria. Please try with different parameters."
        
        # Sort bonds by the upper bound of the yield range
        sorted_bonds = sorted(
            filtered_bonds,
            key=lambda bond: float(bond["yield_range"].split("-")[1].strip("%")),
            reverse=True
        )
        
        # Get the bond with the highest yield
        best_yield_bond = sorted_bonds[0]
        
        # Format best yield bond as a prompt for the LLM
        best_yield_bond_str = f"Bond with the best yield{f' for {term}-year term' if term else ''}:\n\n"
        best_yield_bond_str += f"Issuer: {best_yield_bond['issuer']}\n"
        best_yield_bond_str += f"Rating: {best_yield_bond['rating']}\n"
        best_yield_bond_str += f"Yield Range: {best_yield_bond['yield_range']}\n"
        best_yield_bond_str += f"Maturity: {best_yield_bond['maturity']}\n"
        best_yield_bond_str += f"Available at: {best_yield_bond['available_at']}\n"
        best_yield_bond_str += f"Minimum Investment: {best_yield_bond['min_investment']}\n"
        best_yield_bond_str += f"Face Value: {best_yield_bond['face_value']}\n\n"
        
        best_yield_bond_str += "Other high-yield options:\n\n"
        
        # Create a DataFrame from the top 5 bonds
        df = pd.DataFrame(sorted_bonds[1:5])
        best_yield_bond_str += df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about the bond with the best yield{f' for {term}-year term' if term else ''}:
        
        {best_yield_bond_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Highlight the bond with the best yield and provide information about other high-yield options.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _extract_rating(self, query):
        """
        Extract rating from a query
        
        Args:
            query (str): User query
        
        Returns:
            str: Extracted rating
        """
        # Use the LLM to extract the rating
        prompt = f"""
        Extract the credit rating from the following query:
        
        "{query}"
        
        Respond with just the rating (e.g., AAA, AA+, A), nothing else.
        """
        
        return self.llm_handler.get_completion(prompt, temperature=0.3)
    
    def _get_bonds_by_rating(self, rating):
        """
        Get bonds with a specific rating
        
        Args:
            rating (str): Credit rating
        
        Returns:
            str: Bonds with the specified rating
        """
        # Filter bonds by rating
        rated_bonds = [bond for bond in self.available_bonds if rating.upper() in bond["rating"].upper()]
        
        if not rated_bonds:
            return f"I couldn't find any bonds with a rating of {rating}. Please check the rating and try again."
        
        # Format rated bonds as a prompt for the LLM
        rated_bonds_str = f"Bonds with a rating of {rating}:\n\n"
        
        # Create a DataFrame from the rated bonds
        df = pd.DataFrame(rated_bonds)
        rated_bonds_str += df.to_string(index=False)
        
        # Use the LLM to generate a response
        prompt = f"""
        Based on the following bonds data, provide a comprehensive and well-formatted response to a user asking about bonds with a rating of {rating}:
        
        {rated_bonds_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include information about which platforms offer these bonds and the yield ranges available.
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
        # Use the LLM to extract key entities from the query
        system_message = """
        You are an entity extraction assistant. Your task is to extract key entities from a user query about bonds.
        
        Extract the following entities if present:
        - issuer_name: Name of an issuer
        - min_yield: Minimum yield (as a float)
        - rating: Credit rating (e.g., AAA, AA+)
        - term: Bond term in years (as an integer)
        - platform: Platform name (e.g., SMEST, FixedIncome)
        
        Respond with a JSON object containing the extracted entities.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "issuer_name": {"type": ["string", "null"]},
                "min_yield": {"type": ["number", "null"]},
                "rating": {"type": ["string", "null"]},
                "term": {"type": ["integer", "null"]},
                "platform": {"type": ["string", "null"]}
            }
        }
        
        entities = self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
        
        # Enrich the query with relevant data based on extracted entities
        enriched_query = f"Original query: {query}\n\n"
        
        if entities.get("issuer_name"):
            issuer_bonds = [bond for bond in self.available_bonds if entities["issuer_name"].lower() in bond["issuer"].lower()]
            if issuer_bonds:
                enriched_query += f"Bonds from {entities['issuer_name']} available on our partner platforms:\n"
                df = pd.DataFrame(issuer_bonds)
                enriched_query += df.to_string(index=False)
                enriched_query += "\n\n"
        
        if entities.get("min_yield"):
            high_yield_bonds = []
            for bond in self.available_bonds:
                yield_range = bond["yield_range"]
                lower_bound = float(yield_range.split("-")[0].strip("%"))
                if lower_bound >= entities["min_yield"]:
                    high_yield_bonds.append(bond)
            
            if high_yield_bonds:
                enriched_query += f"Bonds with a yield of {entities['min_yield']}% or higher:\n"
                df = pd.DataFrame(high_yield_bonds)
                enriched_query += df.to_string(index=False)
                enriched_query += "\n\n"
        
        if entities.get("rating"):
            rated_bonds = [bond for bond in self.available_bonds if entities["rating"].upper() in bond["rating"].upper()]
            if rated_bonds:
                enriched_query += f"Bonds with a rating of {entities['rating']}:\n"
                df = pd.DataFrame(rated_bonds)
                enriched_query += df.to_string(index=False)
                enriched_query += "\n\n"
        
        if entities.get("term"):
            target_maturity = str(2023 + entities["term"])  # Assuming current year is 2023
            term_bonds = [bond for bond in self.available_bonds if bond["maturity"] == target_maturity]
            if term_bonds:
                enriched_query += f"Bonds with a {entities['term']}-year term (maturing in {target_maturity}):\n"
                df = pd.DataFrame(term_bonds)
                enriched_query += df.to_string(index=False)
                enriched_query += "\n\n"
        
        if entities.get("platform"):
            platform_bonds = [bond for bond in self.available_bonds if entities["platform"].lower() in bond["available_at"].lower()]
            if platform_bonds:
                enriched_query += f"Bonds available on {entities['platform']}:\n"
                df = pd.DataFrame(platform_bonds)
                enriched_query += df.to_string(index=False)
                enriched_query += "\n\n"
        
        enriched_query += f"Please respond to the user's query: {query}"
        
        return enriched_query 