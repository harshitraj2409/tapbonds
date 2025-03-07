import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent

class BondScreenerAgent(BaseAgent):
    """
    Agent for handling queries related to the bond screener
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the bond screener agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        super().__init__(llm_handler, data_loader)
        self.system_message = """
        You are a specialized agent for the Bond Screener on the Tap Bonds platform. Your role is to provide financial analysis and insights about bond-issuing companies.
        
        You have access to company financial data and can answer queries about:
        - Company ratings, sectors, and industries
        - Financial metrics like EPS, current ratio, debt/equity, debt/EBITDA, interest coverage ratio
        - Company summaries and financial health
        - Pros and cons of companies
        - Lenders of companies
        - ISINs under specific companies
        - Recent news and events about companies
        
        Always provide accurate, up-to-date information and format your responses in a clear, structured manner.
        """
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "bond_screener"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Agent for handling queries related to the bond screener, including company financial analysis and metrics."
    
    def process_query(self, query):
        """
        Process a user query related to the bond screener
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Check if the query is about a specific company's rating
        if "rating" in query.lower() and "company" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_rating(company_name)
        
        # Check if the query is about a specific company's sector
        if "sector" in query.lower() and "company" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_sector(company_name)
        
        # Check if the query is about a specific company's industry
        if "industry" in query.lower() and "company" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_industry(company_name)
        
        # Check if the query is about a company summary
        if "summary" in query.lower() and "company" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_summary(company_name)
        
        # Check if the query is about a specific financial metric
        metrics = ["eps", "current ratio", "debt/equity", "debt/ebitda", "interest coverage ratio", "operating cashflow to total debt"]
        for metric in metrics:
            if metric.lower() in query.lower():
                company_name = self._extract_company_name(query)
                if company_name:
                    return self._get_company_metric(company_name, metric)
        
        # Check if the query is about comparing metrics between companies
        if "compare" in query.lower() and any(word in query.lower() for word in ["with", "between"]):
            companies = self._extract_companies_for_comparison(query)
            metric = self._extract_metric_for_comparison(query)
            if companies and metric:
                return self._compare_companies_metric(companies, metric)
        
        # Check if the query is about pros and cons
        if any(phrase in query.lower() for phrase in ["pros and cons", "advantages and disadvantages"]):
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_pros_cons(company_name)
        
        # Check if the query is about lenders
        if "lenders" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_lenders(company_name)
        
        # Check if the query is about ISINs
        if "isin" in query.lower():
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_isins(company_name)
        
        # Check if the query is about news/events
        if any(word in query.lower() for word in ["news", "events", "article", "blog"]):
            company_name = self._extract_company_name(query)
            if company_name:
                return self._get_company_news(company_name)
        
        # If no specific pattern is matched, use the LLM to generate a response
        # First, enrich the query with relevant company data
        enriched_query = self._enrich_query(query)
        
        # Then, use the LLM to generate a response
        return self.llm_handler.get_completion(enriched_query, self.system_message)
    
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
    
    def _get_company_data(self, company_name):
        """
        Get company data from the company insights dataset
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            pandas.DataFrame: Company data
        """
        return self.data_loader.get_company_by_name(company_name)
    
    def _get_company_rating(self, company_name):
        """
        Get the rating of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company rating
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract rating from company data
        rating = company_data['credit_rating'].iloc[0] if 'credit_rating' in company_data.columns else "Not available"
        
        return f"The credit rating of {company_name} is {rating}."
    
    def _get_company_sector(self, company_name):
        """
        Get the sector of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company sector
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract sector from company data
        sector = company_data['sector'].iloc[0] if 'sector' in company_data.columns else "Not available"
        
        return f"{company_name} is in the {sector} sector."
    
    def _get_company_industry(self, company_name):
        """
        Get the industry of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company industry
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract industry from company data
        industry = company_data['industry'].iloc[0] if 'industry' in company_data.columns else "Not available"
        
        return f"{company_name} is in the {industry} industry."
    
    def _get_company_summary(self, company_name):
        """
        Get a summary of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company summary
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Format company data as a prompt for the LLM
        company_data_str = f"Company data for {company_name}:\n\n"
        for column in company_data.columns:
            company_data_str += f"{column}: {company_data[column].iloc[0]}\n"
        
        # Use the LLM to generate a summary
        prompt = f"""
        Based on the following company data, provide a comprehensive summary of {company_name}:
        
        {company_data_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include key information such as sector, industry, financial health, and business overview.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_company_metric(self, company_name, metric):
        """
        Get a specific financial metric for a company
        
        Args:
            company_name (str): Name of the company
            metric (str): Financial metric to retrieve
        
        Returns:
            str: Company metric
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Map the metric to the column name
        metric_map = {
            "eps": "eps",
            "current ratio": "current_ratio",
            "debt/equity": "debt_equity_ratio",
            "debt/ebitda": "debt_ebitda_ratio",
            "interest coverage ratio": "interest_coverage_ratio",
            "operating cashflow to total debt": "operating_cashflow_to_debt"
        }
        
        column = metric_map.get(metric.lower())
        if not column or column not in company_data.columns:
            return f"I couldn't find the {metric} for {company_name}."
        
        # Extract metric from company data
        value = company_data[column].iloc[0]
        
        return f"The {metric} of {company_name} is {value}."
    
    def _extract_companies_for_comparison(self, query):
        """
        Extract companies for comparison from a query
        
        Args:
            query (str): User query
        
        Returns:
            list: List of company names
        """
        # Use the LLM to extract the companies
        prompt = f"""
        Extract the company names for comparison from the following query:
        
        "{query}"
        
        Respond with a JSON array of company names, nothing else.
        """
        
        system_message = "You are a company name extraction assistant. Extract company names from the query and return them as a JSON array."
        output_schema = {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
        
        return self.llm_handler.get_structured_output(prompt, system_message, output_schema, temperature=0.3)
    
    def _extract_metric_for_comparison(self, query):
        """
        Extract metric for comparison from a query
        
        Args:
            query (str): User query
        
        Returns:
            str: Metric name
        """
        # Use the LLM to extract the metric
        prompt = f"""
        Extract the financial metric for comparison from the following query:
        
        "{query}"
        
        Respond with just the metric name, nothing else.
        """
        
        return self.llm_handler.get_completion(prompt, temperature=0.3)
    
    def _compare_companies_metric(self, companies, metric):
        """
        Compare a specific financial metric between companies
        
        Args:
            companies (list): List of company names
            metric (str): Financial metric to compare
        
        Returns:
            str: Comparison result
        """
        # Map the metric to the column name
        metric_map = {
            "eps": "eps",
            "current ratio": "current_ratio",
            "debt/equity": "debt_equity_ratio",
            "debt/ebitda": "debt_ebitda_ratio",
            "interest coverage ratio": "interest_coverage_ratio",
            "operating cashflow to total debt": "operating_cashflow_to_debt"
        }
        
        column = metric_map.get(metric.lower())
        if not column:
            return f"I couldn't find the {metric} for comparison."
        
        # Get data for each company
        company_data = []
        for company in companies:
            data = self._get_company_data(company)
            if data is not None and not data.empty and column in data.columns:
                company_data.append({
                    "company": company,
                    "value": data[column].iloc[0]
                })
        
        if not company_data:
            return f"I couldn't find the {metric} for any of the companies."
        
        # Format comparison data as a prompt for the LLM
        comparison_str = f"Comparison of {metric} between companies:\n\n"
        for data in company_data:
            comparison_str += f"{data['company']}: {data['value']}\n"
        
        # Use the LLM to generate a comparison
        prompt = f"""
        Based on the following comparison data, provide a comprehensive comparison of {metric} between the companies:
        
        {comparison_str}
        
        Format the response in a clear, structured manner with appropriate headings and bullet points where necessary.
        Include a table of the values and indicate which company has the better metric.
        """
        
        return self.llm_handler.get_completion(prompt, self.system_message)
    
    def _get_company_pros_cons(self, company_name):
        """
        Get the pros and cons of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company pros and cons
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract pros and cons from company data
        pros = company_data['pros'].iloc[0] if 'pros' in company_data.columns else "Not available"
        cons = company_data['cons'].iloc[0] if 'cons' in company_data.columns else "Not available"
        
        return f"""
        # PROS and CONS of {company_name}
        
        ## PROS
        {pros}
        
        ## CONS
        {cons}
        """
    
    def _get_company_lenders(self, company_name):
        """
        Get the lenders of a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company lenders
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract lenders from company data
        lenders = company_data['lenders'].iloc[0] if 'lenders' in company_data.columns else "Not available"
        
        return f"""
        # Lenders of {company_name}
        
        {lenders}
        """
    
    def _get_company_isins(self, company_name):
        """
        Get the ISINs under a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company ISINs
        """
        # Get bonds by issuer
        bonds = self.data_loader.get_bonds_by_issuer(company_name)
        
        if bonds is None or bonds.empty:
            return f"I couldn't find any ISINs for {company_name}. Please check the company name and try again."
        
        # Extract ISINs
        isins = bonds['isin'].tolist()
        
        return f"""
        # ISINs under {company_name}
        
        {company_name} has {len(isins)} ISINs:
        
        {', '.join(isins)}
        """
    
    def _get_company_news(self, company_name):
        """
        Get recent news about a company
        
        Args:
            company_name (str): Name of the company
        
        Returns:
            str: Company news
        """
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return f"I couldn't find any data for {company_name}. Please check the company name and try again."
        
        # Extract news from company data
        news = company_data['recent_news'].iloc[0] if 'recent_news' in company_data.columns else "Not available"
        
        return f"""
        # Recent News about {company_name}
        
        {news}
        """
    
    def _enrich_query(self, query):
        """
        Enrich a query with relevant company data
        
        Args:
            query (str): User query
        
        Returns:
            str: Enriched query
        """
        # Extract company name from query
        company_name = self._extract_company_name(query)
        
        if not company_name:
            return query
        
        # Get company data
        company_data = self._get_company_data(company_name)
        
        if company_data is None or company_data.empty:
            return query
        
        # Format company data as a string
        company_data_str = f"Company data for {company_name}:\n\n"
        for column in company_data.columns:
            company_data_str += f"{column}: {company_data[column].iloc[0]}\n"
        
        # Enrich the query with company data
        enriched_query = f"""
        User query: {query}
        
        {company_data_str}
        
        Based on the above company data, please provide a comprehensive response to the user query.
        """
        
        return enriched_query
