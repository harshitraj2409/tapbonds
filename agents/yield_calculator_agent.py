import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.base_agent import BaseAgent
from utils.calculator import BondCalculator

class YieldCalculatorAgent(BaseAgent):
    """
    Agent for handling queries related to bond yield calculations
    """
    def __init__(self, llm_handler=None, data_loader=None):
        """
        Initialize the yield calculator agent
        
        Args:
            llm_handler (LLMHandler, optional): LLM handler instance. If None, a new one will be created.
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        super().__init__(llm_handler, data_loader)
        self.calculator = BondCalculator(data_loader)
        self.system_message = """
        You are a specialized agent for the Bond Yield Calculator on the Tap Bonds platform. Your role is to help users calculate bond yields, prices, and considerations.
        
        You can perform the following calculations:
        - Calculate the price of a bond based on yield
        - Calculate the yield of a bond based on price
        - Calculate the consideration (total amount) for a bond trade
        - Calculate the clean price of a bond
        
        Always provide accurate calculations and format your responses in a clear, structured manner.
        """
    
    def get_name(self):
        """
        Get the name of the agent
        
        Returns:
            str: Agent name
        """
        return "yield_calculator"
    
    def get_description(self):
        """
        Get the description of the agent
        
        Returns:
            str: Agent description
        """
        return "Agent for handling queries related to bond yield calculations, including price-to-yield and yield-to-price conversions."
    
    def process_query(self, query):
        """
        Process a user query related to bond yield calculations
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Check if the query is about calculating clean price
        if "clean price" in query.lower():
            return self._handle_clean_price_query(query)
        
        # Check if the query is about calculating consideration
        if "consideration" in query.lower():
            return self._handle_consideration_query(query)
        
        # Check if the query is about price to yield calculation
        if "price to yield" in query.lower() or "yield from price" in query.lower():
            return self._handle_price_to_yield_query(query)
        
        # Check if the query is about yield to price calculation
        if "yield to price" in query.lower() or "price from yield" in query.lower():
            return self._handle_yield_to_price_query(query)
        
        # If no specific pattern is matched, extract parameters and determine the calculation type
        params = self._extract_calculation_parameters(query)
        
        if params.get("calculation_type") == "price_from_yield":
            return self._calculate_price_from_yield(params)
        elif params.get("calculation_type") == "yield_from_price":
            return self._calculate_yield_from_price(params)
        elif params.get("calculation_type") == "consideration":
            return self._calculate_consideration(params)
        elif params.get("calculation_type") == "clean_price":
            return self._calculate_clean_price(params)
        
        # If parameters couldn't be extracted, ask for more information
        return self._ask_for_calculation_parameters(query)
    
    def _handle_clean_price_query(self, query):
        """
        Handle a query about calculating clean price
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Try to extract parameters from the query
        params = self._extract_clean_price_parameters(query)
        
        if params.get("isin") and params.get("trade_date") and params.get("units"):
            return self._calculate_clean_price(params)
        
        return """
        # How to Calculate Clean Price of a Bond

        The clean price of a bond is the price excluding accrued interest. To calculate it, I need the following information:

        1. **ISIN of the bond** - This is the unique identifier for the bond
        2. **Trade date** - The date on which you want to calculate the clean price (YYYY-MM-DD)
        3. **Number of units** - How many units of the bond you're considering
        4. **Expected yield** (optional) - The yield rate you want to use for calculation (%)

        ## Example
        For a bond with:
        - ISIN: INE08XP07258
        - Trade date: 2025-03-03
        - Units: 20
        - Yield: 15.10%

        The calculation would give a clean price of 96.25% of face value.

        ## Would you like me to calculate the clean price for a specific bond?
        Please provide the ISIN, trade date, number of units, and optionally the yield rate.
        """
    
    def _handle_consideration_query(self, query):
        """
        Handle a query about calculating consideration
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Try to extract parameters from the query
        params = self._extract_consideration_parameters(query)
        
        if params.get("isin") and params.get("trade_date") and params.get("units"):
            return self._calculate_consideration(params)
        
        return """
        # How to Calculate Consideration for a Bond

        The consideration is the total amount payable for a bond purchase, including accrued interest. To calculate it, I need:

        1. **ISIN of the bond** - This is the unique identifier for the bond
        2. **Trade date** - The date on which the trade will occur (YYYY-MM-DD)
        3. **Number of units** - How many units of the bond you're trading

        ## Example
        For a bond with:
        - ISIN: INE08XP07258
        - Trade date: 2025-03-03
        - Units: 20

        The calculation would give:
        - Clean Price: 96.25% of face value
        - Accrued Interest: ₹4,936.44
        - Total Consideration: ₹1,929,966.44
        - Stamp Duty: ₹2.00
        - Final Consideration: ₹1,929,968.44

        ## Would you like me to calculate the consideration for a specific bond?
        Please provide the ISIN, trade date, and number of units.
        """
    
    def _handle_price_to_yield_query(self, query):
        """
        Handle a query about calculating yield from price
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Try to extract parameters from the query
        params = self._extract_price_to_yield_parameters(query)
        
        if params.get("isin") and params.get("investment_date") and params.get("units") and params.get("price"):
            return self._calculate_yield_from_price(params)
        
        return """
        # How to Calculate Yield from Price

        To calculate the yield of a bond based on its price, I need:

        1. **ISIN of the bond** - This is the unique identifier for the bond
        2. **Investment date** - The date on which you're investing (YYYY-MM-DD)
        3. **Number of units** - How many units of the bond you're purchasing
        4. **Price** - The clean price as a percentage of face value (e.g., 98.5 for 98.5%)

        ## Example
        For a bond with:
        - ISIN: INE08XP07258
        - Investment date: 2025-03-03
        - Units: 20
        - Price: 96.25

        The calculation would give a yield of approximately 15.10%.

        ## Would you like me to calculate the yield for a specific bond?
        Please provide the ISIN, investment date, number of units, and price.
        """
    
    def _handle_yield_to_price_query(self, query):
        """
        Handle a query about calculating price from yield
        
        Args:
            query (str): User query
        
        Returns:
            str: Response to the query
        """
        # Try to extract parameters from the query
        params = self._extract_yield_to_price_parameters(query)
        
        if params.get("isin") and params.get("investment_date") and params.get("units") and params.get("yield_rate"):
            return self._calculate_price_from_yield(params)
        
        return """
        # How to Calculate Price from Yield

        To calculate the price of a bond based on its yield, I need:

        1. **ISIN of the bond** - This is the unique identifier for the bond
        2. **Investment date** - The date on which you're investing (YYYY-MM-DD)
        3. **Number of units** - How many units of the bond you're purchasing
        4. **Expected yield** - The yield rate you want to use for calculation (%)

        ## Example
        For a bond with:
        - ISIN: INE08XP07258
        - Investment date: 2025-03-03
        - Units: 20
        - Yield: 15.10%

        The calculation would give a clean price of 96.25% of face value.

        ## Would you like me to calculate the price for a specific bond?
        Please provide the ISIN, investment date, number of units, and expected yield.
        """
    
    def _extract_calculation_parameters(self, query):
        """
        Extract calculation parameters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted parameters
        """
        # Use the LLM to extract parameters
        system_message = """
        You are a parameter extraction assistant for bond calculations. Your task is to extract calculation parameters from a user query.
        
        Extract the following parameters if present:
        - calculation_type: Type of calculation ('price_from_yield', 'yield_from_price', 'consideration', or 'clean_price')
        - isin: ISIN of the bond
        - investment_date or trade_date: Date for the calculation (YYYY-MM-DD)
        - units: Number of units
        - yield_rate: Expected yield (%) (for price_from_yield or clean_price)
        - price: Price per unit as percentage of face value (for yield_from_price)
        
        Respond with a JSON object containing the extracted parameters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "calculation_type": {
                    "type": "string",
                    "enum": ["price_from_yield", "yield_from_price", "consideration", "clean_price"]
                },
                "isin": {"type": ["string", "null"]},
                "investment_date": {"type": ["string", "null"]},
                "trade_date": {"type": ["string", "null"]},
                "units": {"type": ["integer", "null"]},
                "yield_rate": {"type": ["number", "null"]},
                "price": {"type": ["number", "null"]}
            }
        }
        
        return self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
    
    def _extract_clean_price_parameters(self, query):
        """
        Extract clean price calculation parameters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted parameters
        """
        # Use the LLM to extract parameters
        system_message = """
        You are a parameter extraction assistant for bond clean price calculations. Your task is to extract calculation parameters from a user query.
        
        Extract the following parameters if present:
        - isin: ISIN of the bond
        - trade_date: Date for the calculation (YYYY-MM-DD)
        - units: Number of units
        - yield_rate: Expected yield (%) (optional)
        
        Respond with a JSON object containing the extracted parameters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "isin": {"type": ["string", "null"]},
                "trade_date": {"type": ["string", "null"]},
                "units": {"type": ["integer", "null"]},
                "yield_rate": {"type": ["number", "null"]}
            }
        }
        
        params = self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
        params["calculation_type"] = "clean_price"
        return params
    
    def _extract_consideration_parameters(self, query):
        """
        Extract consideration calculation parameters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted parameters
        """
        # Use the LLM to extract parameters
        system_message = """
        You are a parameter extraction assistant for bond consideration calculations. Your task is to extract calculation parameters from a user query.
        
        Extract the following parameters if present:
        - isin: ISIN of the bond
        - trade_date: Date for the calculation (YYYY-MM-DD)
        - units: Number of units
        
        Respond with a JSON object containing the extracted parameters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "isin": {"type": ["string", "null"]},
                "trade_date": {"type": ["string", "null"]},
                "units": {"type": ["integer", "null"]}
            }
        }
        
        params = self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
        params["calculation_type"] = "consideration"
        return params
    
    def _extract_price_to_yield_parameters(self, query):
        """
        Extract price to yield calculation parameters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted parameters
        """
        # Use the LLM to extract parameters
        system_message = """
        You are a parameter extraction assistant for bond yield calculations. Your task is to extract calculation parameters from a user query.
        
        Extract the following parameters if present:
        - isin: ISIN of the bond
        - investment_date: Date for the calculation (YYYY-MM-DD)
        - units: Number of units
        - price: Price per unit as percentage of face value (e.g., 98.5 for 98.5%)
        
        Respond with a JSON object containing the extracted parameters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "isin": {"type": ["string", "null"]},
                "investment_date": {"type": ["string", "null"]},
                "units": {"type": ["integer", "null"]},
                "price": {"type": ["number", "null"]}
            }
        }
        
        params = self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
        params["calculation_type"] = "yield_from_price"
        return params
    
    def _extract_yield_to_price_parameters(self, query):
        """
        Extract yield to price calculation parameters from a query
        
        Args:
            query (str): User query
        
        Returns:
            dict: Extracted parameters
        """
        # Use the LLM to extract parameters
        system_message = """
        You are a parameter extraction assistant for bond price calculations. Your task is to extract calculation parameters from a user query.
        
        Extract the following parameters if present:
        - isin: ISIN of the bond
        - investment_date: Date for the calculation (YYYY-MM-DD)
        - units: Number of units
        - yield_rate: Expected yield (%)
        
        Respond with a JSON object containing the extracted parameters.
        """
        
        output_schema = {
            "type": "object",
            "properties": {
                "isin": {"type": ["string", "null"]},
                "investment_date": {"type": ["string", "null"]},
                "units": {"type": ["integer", "null"]},
                "yield_rate": {"type": ["number", "null"]}
            }
        }
        
        params = self.llm_handler.get_structured_output(query, system_message, output_schema, temperature=0.3)
        params["calculation_type"] = "price_from_yield"
        return params
    
    def _calculate_price_from_yield(self, params):
        """
        Calculate price from yield
        
        Args:
            params (dict): Calculation parameters
        
        Returns:
            str: Calculation result
        """
        isin = params.get("isin")
        investment_date = params.get("investment_date")
        units = params.get("units")
        yield_rate = params.get("yield_rate")
        
        if not isin or not investment_date or not units or not yield_rate:
            return """
            # Price from Yield Calculation

            To calculate the price from a bond yield, I need the following information:
            
            1. **ISIN of the bond** - This is the unique identifier for the bond
            2. **Investment date** - The date on which you're investing (YYYY-MM-DD)
            3. **Number of units** - How many units of the bond you're purchasing
            4. **Expected yield** - The yield rate you want to use for calculation (%)
            
            Please provide this information, and I'll calculate the price for you.
            """
        
        result = self.calculator.calculate_price_from_yield(isin, investment_date, units, yield_rate)
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        # Format the result as a response
        response = f"""
        # Price Calculation Result for ISIN {isin}
        
        ## Input Parameters
        - Investment Date: {result['investment_date']}
        - Number of Units: {result['units']}
        - Expected Yield: {result['yield_rate']}%
        
        ## Bond Details
        - Face Value: ₹{result['face_value']:,.2f}
        - Coupon Rate: {result['coupon_rate']}%
        - Maturity Date: {result['maturity_date']}
        
        ## Calculation Result
        - Clean Price: {result['clean_price']:.4f}% of face value
        - Accrued Interest: ₹{result['accrued_interest']:,.2f}
        - Dirty Price: {result['dirty_price']:.4f}% of face value
        
        ## Total Amount
        - Price Per Unit: ₹{result['price_per_unit']:,.2f}
        - Consideration (Clean): ₹{result['consideration']:,.2f}
        - Total Consideration (Dirty): ₹{result['total_consideration']:,.2f}
        
        ## Future Cash Flows
        """
        
        # Add cash flow table
        response += "| Date | Cash Flow Amount | Days | Present Value |\n"
        response += "| ---- | --------------- | ---- | ------------- |\n"
        
        for cf in result['future_cashflows']:
            response += f"| {cf['cash_flow_date']} | ₹{float(cf['cash_flow_amount']):,.2f} | {cf['days']} | ₹{cf['present_value']:,.2f} |\n"
        
        return response
    
    def _calculate_yield_from_price(self, params):
        """
        Calculate yield from price
        
        Args:
            params (dict): Calculation parameters
        
        Returns:
            str: Calculation result
        """
        isin = params.get("isin")
        investment_date = params.get("investment_date")
        units = params.get("units")
        price = params.get("price")
        
        if not isin or not investment_date or not units or not price:
            return """
            # Yield from Price Calculation

            To calculate the yield from a bond price, I need the following information:
            
            1. **ISIN of the bond** - This is the unique identifier for the bond
            2. **Investment date** - The date on which you're investing (YYYY-MM-DD)
            3. **Number of units** - How many units of the bond you're purchasing
            4. **Price** - The clean price as a percentage of face value (e.g., 98.5 for 98.5%)
            
            Please provide this information, and I'll calculate the yield for you.
            """
        
        result = self.calculator.calculate_yield_from_price(isin, investment_date, units, price)
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        # Format the result as a response
        response = f"""
        # Yield Calculation Result for ISIN {isin}
        
        ## Input Parameters
        - Investment Date: {result['investment_date']}
        - Number of Units: {result['units']}
        - Clean Price: {result['clean_price']:.4f}% of face value
        
        ## Bond Details
        - Face Value: ₹{result['face_value']:,.2f}
        - Coupon Rate: {result['coupon_rate']}%
        - Maturity Date: {result['maturity_date']}
        
        ## Calculation Result
        - Yield Rate: {result['yield_rate']:.4f}%
        - Accrued Interest: ₹{result['accrued_interest']:,.2f}
        - Dirty Price: {result['dirty_price']:.4f}% of face value
        
        ## Total Amount
        - Price Per Unit: ₹{result['price_per_unit']:,.2f}
        - Consideration (Clean): ₹{result['consideration']:,.2f}
        - Total Consideration (Dirty): ₹{result['total_consideration']:,.2f}
        
        ## Future Cash Flows
        """
        
        # Add cash flow table
        response += "| Date | Cash Flow Amount | Days | Present Value |\n"
        response += "| ---- | --------------- | ---- | ------------- |\n"
        
        for cf in result['future_cashflows']:
            response += f"| {cf['cash_flow_date']} | ₹{float(cf['cash_flow_amount']):,.2f} | {cf['days']} | ₹{cf['present_value']:,.2f} |\n"
        
        return response
    
    def _calculate_consideration(self, params):
        """
        Calculate consideration
        
        Args:
            params (dict): Calculation parameters
        
        Returns:
            str: Calculation result
        """
        isin = params.get("isin")
        trade_date = params.get("trade_date")
        units = params.get("units")
        
        if not isin or not trade_date or not units:
            return """
            # Consideration Calculation

            To calculate the consideration for a bond, I need the following information:
            
            1. **ISIN of the bond** - This is the unique identifier for the bond
            2. **Trade date** - The date on which the trade will occur (YYYY-MM-DD)
            3. **Number of units** - How many units of the bond you're trading
            
            Please provide this information, and I'll calculate the consideration for you.
            """
        
        result = self.calculator.calculate_consideration(isin, trade_date, units)
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        # Format the result as a response
        response = f"""
        # Consideration Calculation Result for ISIN {isin}
        
        ## Input Parameters
        - Trade Date: {result['trade_date']}
        - Number of Units: {result['units']}
        
        ## Bond Details
        - Face Value: ₹{result['face_value']:,.2f}
        - Market Yield: {result['market_yield']:.4f}%
        
        ## Price Components
        - Clean Price: {result['clean_price']:.4f}% of face value
        - Accrued Interest: ₹{result['accrued_interest']:,.2f}
        - Dirty Price: {result['dirty_price']:.4f}% of face value
        
        ## Total Amount
        - Consideration (Clean): ₹{result['consideration']:,.2f}
        - Total Consideration (Dirty): ₹{result['total_consideration']:,.2f}
        - Stamp Duty: ₹{result['stamp_duty']:,.2f}
        - Final Consideration: ₹{result['final_consideration']:,.2f}
        """
        
        return response
    
    def _calculate_clean_price(self, params):
        """
        Calculate clean price
        
        Args:
            params (dict): Calculation parameters
        
        Returns:
            str: Calculation result
        """
        isin = params.get("isin")
        trade_date = params.get("trade_date")
        units = params.get("units")
        yield_rate = params.get("yield_rate")
        
        if not isin or not trade_date or not units:
            return """
            # Clean Price Calculation

            To calculate the clean price of a bond, I need the following information:
            
            1. **ISIN of the bond** - This is the unique identifier for the bond
            2. **Trade date** - The date on which you want to calculate the clean price (YYYY-MM-DD)
            3. **Number of units** - How many units of the bond you're considering
            4. **Expected yield** (optional) - The yield rate you want to use for calculation (%)
            
            Please provide this information, and I'll calculate the clean price for you.
            """
        
        result = self.calculator.calculate_clean_price(isin, trade_date, units, yield_rate)
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        # Format the result as a response
        response = f"""
        # Clean Price Calculation Result for ISIN {isin}
        
        ## Input Parameters
        - Trade Date: {result['trade_date']}
        - Number of Units: {result['units']}
        - Yield Rate: {result['yield_rate']}%
        
        ## Bond Details
        - Face Value: ₹{result['face_value']:,.2f}
        - Coupon Rate: {result['coupon_rate']}%
        - Maturity Date: {result['maturity_date']}
        
        ## Calculation Result
        - Clean Price: {result['clean_price']:.4f}% of face value
        
        This means that the clean price of the bond is {result['clean_price']:.4f}% of its face value.
        For a face value of ₹{result['face_value']:,.2f}, the clean price per unit is ₹{(result['clean_price'] * result['face_value'] / 100):,.2f}.
        """
        
        return response
    
    def _ask_for_calculation_parameters(self, query):
        """
        Ask for calculation parameters
        
        Args:
            query (str): User query
        
        Returns:
            str: Response asking for parameters
        """
        return """
        # Bond Calculator

        I can help you with various bond calculations. Please let me know which calculation you'd like to perform:

        ## 1. Calculate Clean Price
        The clean price is the price of a bond excluding accrued interest.
        
        ## 2. Calculate Consideration
        The consideration is the total amount payable for a bond purchase, including accrued interest.
        
        ## 3. Calculate Yield from Price
        This calculates the yield of a bond based on its price.
        
        ## 4. Calculate Price from Yield
        This calculates the price of a bond based on its yield.

        For any of these calculations, I'll need specific information such as the bond's ISIN, trade date, and number of units.

        Which calculation would you like to perform?
        """ 