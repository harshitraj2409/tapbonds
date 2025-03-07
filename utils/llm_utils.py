import os
import sys
import json
from openai import OpenAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, MODEL_NAME

class LLMHandler:
    """
    Utility class for handling LLM interactions
    """
    def __init__(self, api_key=None, model_name=None):
        """
        Initialize the LLM handler
        
        Args:
            api_key (str, optional): OpenAI API key. If None, will use the one from config.
            model_name (str, optional): Model name to use. If None, will use the one from config.
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model_name = model_name or MODEL_NAME
        self.client = OpenAI(api_key=self.api_key)
    
    def get_completion(self, prompt, system_message=None, temperature=0.7, max_tokens=1000):
        """
        Get a completion from the LLM
        
        Args:
            prompt (str): User prompt
            system_message (str, optional): System message to use
            temperature (float, optional): Temperature for generation
            max_tokens (int, optional): Maximum tokens to generate
        
        Returns:
            str: Generated text
        """
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error getting completion: {str(e)}"
    
    def get_structured_output(self, prompt, system_message=None, output_schema=None, temperature=0.7):
        """
        Get a structured output from the LLM
        
        Args:
            prompt (str): User prompt
            system_message (str, optional): System message to use
            output_schema (dict, optional): JSON schema for the output
            temperature (float, optional): Temperature for generation
        
        Returns:
            dict: Structured output
        """
        try:
            messages = []
            
            if system_message:
                if output_schema:
                    system_message += f"\n\nYou must respond with a JSON object that conforms to the following schema:\n{json.dumps(output_schema, indent=2)}"
                
                messages.append({"role": "system", "content": system_message})
            elif output_schema:
                messages.append({
                    "role": "system", 
                    "content": f"You must respond with a JSON object that conforms to the following schema:\n{json.dumps(output_schema, indent=2)}"
                })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        
        except Exception as e:
            return {"error": f"Error getting structured output: {str(e)}"}
    
    def classify_query(self, query):
        """
        Classify a user query to determine which agent should handle it
        
        Args:
            query (str): User query
        
        Returns:
            dict: Classification result
        """
        system_message = """
        You are a query classifier for a bond investment platform. Your task is to analyze the user's query and determine which specialized agent should handle it.
        
        The available agents are:
        1. bonds_directory - For queries about bond details, ISIN lookups, issuer information, etc.
        2. bond_finder - For queries about comparing bonds across platforms, finding best yields, etc.
        3. cashflow_maturity - For queries about bond cash flows, maturity schedules, payment timelines, etc.
        4. bond_screener - For queries about company-level financial analysis, metrics, etc.
        5. yield_calculator - For queries about calculating bond yields, prices, considerations, etc.
        
        You must respond with a JSON object containing the agent name and confidence score.
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
        
        return self.get_structured_output(query, system_message, output_schema, temperature=0.3) 