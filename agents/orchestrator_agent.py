import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from agents.bonds_directory_agent import BondsDirectoryAgent
from agents.bond_finder_agent import BondFinderAgent
from agents.cashflow_maturity_agent import CashflowMaturityAgent
from agents.bond_screener_agent import BondScreenerAgent
from agents.yield_calculator_agent import YieldCalculatorAgent
from utils.llm_utils import LLMHandler
from utils.data_loader import DataLoader

class OrchestratorAgent:
    """
    Orchestrator agent that routes queries to the appropriate specialized agent
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the orchestrator agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        self.llm_handler = llm_handler if llm_handler else LLMHandler()
        self.data_loader = data_loader if data_loader else DataLoader()
        
        # Initialize specialized agents
        self.agents = {
            "bonds_directory": BondsDirectoryAgent(self.llm_handler, self.data_loader),
            "bond_finder": BondFinderAgent(self.llm_handler, self.data_loader),
            "cashflow_maturity": CashflowMaturityAgent(self.llm_handler, self.data_loader),
            "bond_screener": BondScreenerAgent(self.llm_handler, self.data_loader),
            "yield_calculator": YieldCalculatorAgent(self.llm_handler, self.data_loader)
        }
        
        self.system_message = """
        You are the main orchestrator agent for the Tap Bonds platform. Your role is to analyze user queries and route them to the appropriate specialized agent.
        
        The available agents are:
        1. bonds_directory - For queries about bond details, ISIN lookups, issuer information, etc.
        2. bond_finder - For queries about comparing bonds across platforms, finding best yields, etc.
        3. cashflow_maturity - For queries about bond cash flows, maturity schedules, payment timelines, etc.
        4. bond_screener - For queries about company-level financial analysis, metrics, etc.
        5. yield_calculator - For queries about calculating bond yields, prices, considerations, etc.
        
        Analyze the user query carefully and determine which agent would be best suited to handle it.
        """
    
    def process_query(self, query):
        """
        Process a user query by routing it to the appropriate specialized agent
        
        Args:
            query (str): User query
        
        Returns:
            dict: Response containing the agent used and the response
        """
        # Classify the query to determine which agent should handle it
        classification = self.llm_handler.classify_query(query)
        
        agent_name = classification.get("agent")
        confidence = classification.get("confidence", 0)
        explanation = classification.get("explanation", "")
        
        # If confidence is low, use a more detailed prompt to classify
        if confidence < 0.7:
            classification = self._detailed_classification(query)
            agent_name = classification.get("agent")
            confidence = classification.get("confidence", 0)
            explanation = classification.get("explanation", "")
        
        # Get the appropriate agent
        agent = self.agents.get(agent_name)
        
        if not agent:
            # If no agent is found, use a fallback approach
            return {
                "agent": "fallback",
                "response": "I'm not sure which specialized agent can best help with your query. Could you please provide more specific details about what you're looking for?",
                "confidence": 0,
                "explanation": "No suitable agent found"
            }
        
        # Process the query with the selected agent
        response = agent.process_query(query)
        
        return {
            "agent": agent_name,
            "response": response,
            "confidence": confidence,
            "explanation": explanation
        }
    
    def _detailed_classification(self, query):
        """
        Perform a more detailed classification of the query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Classification result
        """
        system_message = """
        You are a query classifier for a bond investment platform. Your task is to analyze the user's query in detail and determine which specialized agent should handle it.
        
        The available agents are:
        
        1. bonds_directory - For queries about:
           - Bond details by ISIN
           - Bonds issued by a specific company
           - Filtering bonds by criteria (coupon rate, maturity date, credit rating, etc.)
           - Security details of bonds
           - Debenture trustees
           - Listing exchanges and trading status
           - Face values and other bond parameters
        
        2. bond_finder - For queries about:
           - Comparing bonds across platforms
           - Finding the best yields
           - Platform availability of bonds
           - Yield-based searches
           - Credit rating-based searches
        
        3. cashflow_maturity - For queries about:
           - Bond cash flows
           - Maturity schedules
           - Payment timelines
           - Interest payment dates
        
        4. bond_screener - For queries about:
           - Company-level financial analysis
           - Company ratings, sectors, and industries
           - Financial metrics (EPS, current ratio, debt/equity, etc.)
           - Company summaries
           - Pros and cons of companies
           - Lenders of companies
           - ISINs under specific companies
           - Recent news about companies
        
        5. yield_calculator - For queries about:
           - Calculating bond yields
           - Calculating bond prices
           - Calculating considerations
           - Clean price calculations
        
        Analyze the query carefully and determine which agent would be best suited to handle it.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "agent": {
                    "type": "string",
                    "enum": ["bonds_directory", "bond_finder", "cashflow_maturity", "bond_screener", "yield_calculator"]
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "explanation": {
                    "type": "string"
                }
            },
            "required": ["agent", "confidence", "explanation"]
        }
        
        return self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3) 