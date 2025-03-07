import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_utils import LLMHandler
from utils.data_loader import DataLoader

class BaseAgent:
    """
    Base class for all agents
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the base agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        self.llm_handler = llm_handler if llm_handler else LLMHandler()
        self.data_loader = data_loader if data_loader else DataLoader()
        self.system_message = "You are a helpful assistant for a bond investment platform."
    
    def process_query(self, query):
        """
        Process a user query
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # This method should be overridden by subclasses
        return self.llm_handler.get_completion(query, self.system_message)
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "base_agent"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Base agent for the bond investment platform." 