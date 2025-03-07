import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import DataLoader

class BondCalculator:
    """
    Utility class for bond yield and price calculations
    """
    def __init__(self, data_loader=None):
        """
        Initialize the calculator with a data loader
        
        Args:
            data_loader (DataLoader, optional): Data loader instance. If None, a new one will be created.
        """
        self.data_loader = data_loader if data_loader else DataLoader()
    
    def calculate_price_from_yield(self, isin, investment_date, units, yield_rate):
        """
        Calculate the price of a bond based on the yield
        
        Args:
            isin (str): ISIN of the bond
            investment_date (str): Date of investment (YYYY-MM-DD)
            units (int): Number of units to invest
            yield_rate (float): Expected yield rate (in percentage)
        
        Returns:
            dict: Dictionary containing price and other details
        """
        try:
            # Get bond details
            bond_details = self.data_loader.get_bond_by_isin(isin)
            if bond_details.empty:
                return {"error": f"Bond with ISIN {isin} not found"}
            
            # Get cashflows
            cashflows = self.data_loader.get_cashflows_by_isin(isin)
            if cashflows.empty:
                return {"error": f"Cashflows for ISIN {isin} not found"}
            
            # Convert investment date to datetime
            investment_date = pd.to_datetime(investment_date)
            
            # Filter cashflows after investment date
            future_cashflows = cashflows[pd.to_datetime(cashflows['cash_flow_date']) > investment_date]
            
            if future_cashflows.empty:
                return {"error": "No future cashflows found for this bond"}
            
            # Calculate days to each cashflow
            future_cashflows['days'] = (pd.to_datetime(future_cashflows['cash_flow_date']) - investment_date).dt.days
            
            # Calculate present value of each cashflow
            yield_rate_decimal = yield_rate / 100
            future_cashflows['present_value'] = future_cashflows.apply(
                lambda row: float(row['cash_flow_amount']) / ((1 + yield_rate_decimal) ** (row['days'] / 365)),
                axis=1
            )
            
            # Calculate total present value (price)
            price_per_unit = future_cashflows['present_value'].sum()
            total_price = price_per_unit * units
            
            # Get bond details
            face_value = float(bond_details['face_value'].iloc[0]) if 'face_value' in bond_details.columns else 100000
            coupon_rate = float(bond_details['coupon_rate'].iloc[0]) if 'coupon_rate' in bond_details.columns else None
            maturity_date = bond_details['maturity_date'].iloc[0] if 'maturity_date' in bond_details.columns else None
            
            # Calculate clean price as percentage of face value
            clean_price = (price_per_unit / face_value) * 100
            
            # Calculate accrued interest
            accrued_interest = self._calculate_accrued_interest(isin, investment_date)
            
            # Calculate dirty price
            dirty_price = clean_price + (accrued_interest / face_value) * 100
            
            # Calculate consideration
            consideration = (clean_price * face_value / 100) * units
            total_consideration = consideration + (accrued_interest * units)
            
            return {
                "isin": isin,
                "investment_date": investment_date.strftime('%Y-%m-%d'),
                "units": units,
                "yield_rate": yield_rate,
                "face_value": face_value,
                "coupon_rate": coupon_rate,
                "maturity_date": maturity_date,
                "price_per_unit": price_per_unit,
                "total_price": total_price,
                "clean_price": clean_price,
                "accrued_interest": accrued_interest,
                "dirty_price": dirty_price,
                "consideration": consideration,
                "total_consideration": total_consideration,
                "future_cashflows": future_cashflows[['cash_flow_date', 'cash_flow_amount', 'days', 'present_value']].to_dict('records')
            }
        
        except Exception as e:
            return {"error": f"Error calculating price: {str(e)}"}
    
    def calculate_yield_from_price(self, isin, investment_date, units, price):
        """
        Calculate the yield of a bond based on the price
        
        Args:
            isin (str): ISIN of the bond
            investment_date (str): Date of investment (YYYY-MM-DD)
            units (int): Number of units to invest
            price (float): Price per unit (as percentage of face value)
        
        Returns:
            dict: Dictionary containing yield and other details
        """
        try:
            # Get bond details
            bond_details = self.data_loader.get_bond_by_isin(isin)
            if bond_details.empty:
                return {"error": f"Bond with ISIN {isin} not found"}
            
            # Get cashflows
            cashflows = self.data_loader.get_cashflows_by_isin(isin)
            if cashflows.empty:
                return {"error": f"Cashflows for ISIN {isin} not found"}
            
            # Convert investment date to datetime
            investment_date = pd.to_datetime(investment_date)
            
            # Filter cashflows after investment date
            future_cashflows = cashflows[pd.to_datetime(cashflows['cash_flow_date']) > investment_date]
            
            if future_cashflows.empty:
                return {"error": "No future cashflows found for this bond"}
            
            # Get face value
            face_value = float(bond_details['face_value'].iloc[0]) if 'face_value' in bond_details.columns else 100000
            
            # Calculate actual price per unit based on percentage
            price_per_unit = (price / 100) * face_value
            
            # Calculate days to each cashflow
            future_cashflows['days'] = (pd.to_datetime(future_cashflows['cash_flow_date']) - investment_date).dt.days
            
            # Function to calculate NPV given a yield rate
            def calculate_npv(yield_rate):
                return sum(
                    float(row['cash_flow_amount']) / ((1 + yield_rate) ** (row['days'] / 365))
                    for _, row in future_cashflows.iterrows()
                ) - price_per_unit
            
            # Find yield rate using numerical methods (bisection)
            lower_yield = 0.0001  # 0.01%
            upper_yield = 1.0  # 100%
            tolerance = 0.0001
            max_iterations = 100
            
            for _ in range(max_iterations):
                mid_yield = (lower_yield + upper_yield) / 2
                npv = calculate_npv(mid_yield)
                
                if abs(npv) < tolerance:
                    break
                
                if npv > 0:
                    lower_yield = mid_yield
                else:
                    upper_yield = mid_yield
            
            yield_rate = mid_yield * 100  # Convert to percentage
            
            # Get bond details
            coupon_rate = float(bond_details['coupon_rate'].iloc[0]) if 'coupon_rate' in bond_details.columns else None
            maturity_date = bond_details['maturity_date'].iloc[0] if 'maturity_date' in bond_details.columns else None
            
            # Calculate present value of each cashflow with the calculated yield
            future_cashflows['present_value'] = future_cashflows.apply(
                lambda row: float(row['cash_flow_amount']) / ((1 + (yield_rate / 100)) ** (row['days'] / 365)),
                axis=1
            )
            
            # Calculate accrued interest
            accrued_interest = self._calculate_accrued_interest(isin, investment_date)
            
            # Calculate clean price
            clean_price = price
            
            # Calculate dirty price
            dirty_price = clean_price + (accrued_interest / face_value) * 100
            
            # Calculate consideration
            consideration = (clean_price * face_value / 100) * units
            total_consideration = consideration + (accrued_interest * units)
            
            return {
                "isin": isin,
                "investment_date": investment_date.strftime('%Y-%m-%d'),
                "units": units,
                "price_per_unit": price_per_unit,
                "total_price": price_per_unit * units,
                "yield_rate": yield_rate,
                "face_value": face_value,
                "coupon_rate": coupon_rate,
                "maturity_date": maturity_date,
                "clean_price": clean_price,
                "accrued_interest": accrued_interest,
                "dirty_price": dirty_price,
                "consideration": consideration,
                "total_consideration": total_consideration,
                "future_cashflows": future_cashflows[['cash_flow_date', 'cash_flow_amount', 'days', 'present_value']].to_dict('records')
            }
        
        except Exception as e:
            return {"error": f"Error calculating yield: {str(e)}"}
    
    def calculate_consideration(self, isin, trade_date, units):
        """
        Calculate the consideration (total amount) for a bond trade
        
        Args:
            isin (str): ISIN of the bond
            trade_date (str): Date of trade (YYYY-MM-DD)
            units (int): Number of units to trade
        
        Returns:
            dict: Dictionary containing consideration and other details
        """
        try:
            # Get bond details
            bond_details = self.data_loader.get_bond_by_isin(isin)
            if bond_details.empty:
                return {"error": f"Bond with ISIN {isin} not found"}
            
            # Get face value
            face_value = float(bond_details['face_value'].iloc[0]) if 'face_value' in bond_details.columns else 100000
            
            # Get cashflows
            cashflows = self.data_loader.get_cashflows_by_isin(isin)
            if cashflows.empty:
                return {"error": f"Cashflows for ISIN {isin} not found"}
            
            # Convert trade date to datetime
            trade_date = pd.to_datetime(trade_date)
            
            # Calculate yield (assuming market yield)
            market_yield = float(bond_details['yield'].iloc[0]) if 'yield' in bond_details.columns else 10.0
            
            # Calculate price using yield
            result = self.calculate_price_from_yield(isin, trade_date.strftime('%Y-%m-%d'), units, market_yield)
            
            if "error" in result:
                return {"error": result["error"]}
            
            # Extract relevant information
            clean_price = result["clean_price"]
            accrued_interest = result["accrued_interest"]
            dirty_price = result["dirty_price"]
            consideration = result["consideration"]
            total_consideration = result["total_consideration"]
            
            # Calculate stamp duty (assuming 0.0001% of consideration)
            stamp_duty = round(total_consideration * 0.000001, 2)
            if stamp_duty < 1:
                stamp_duty = 1
            
            # Add stamp duty to total consideration
            final_consideration = total_consideration + stamp_duty
            
            return {
                "isin": isin,
                "trade_date": trade_date.strftime('%Y-%m-%d'),
                "units": units,
                "face_value": face_value,
                "market_yield": market_yield,
                "clean_price": clean_price,
                "accrued_interest": accrued_interest,
                "dirty_price": dirty_price,
                "consideration": consideration,
                "total_consideration": total_consideration,
                "stamp_duty": stamp_duty,
                "final_consideration": final_consideration
            }
        
        except Exception as e:
            return {"error": f"Error calculating consideration: {str(e)}"}
    
    def calculate_clean_price(self, isin, trade_date, units, yield_rate=None):
        """
        Calculate the clean price of a bond
        
        Args:
            isin (str): ISIN of the bond
            trade_date (str): Date of trade (YYYY-MM-DD)
            units (int): Number of units to trade
            yield_rate (float, optional): Yield rate to use for calculation. If None, market yield will be used.
        
        Returns:
            dict: Dictionary containing clean price and other details
        """
        try:
            # Get bond details
            bond_details = self.data_loader.get_bond_by_isin(isin)
            if bond_details.empty:
                return {"error": f"Bond with ISIN {isin} not found"}
            
            # Get yield rate
            if yield_rate is None:
                yield_rate = float(bond_details['yield'].iloc[0]) if 'yield' in bond_details.columns else 10.0
            
            # Calculate price using yield
            result = self.calculate_price_from_yield(isin, trade_date, units, yield_rate)
            
            if "error" in result:
                return {"error": result["error"]}
            
            # Extract clean price
            clean_price = result["clean_price"]
            
            return {
                "isin": isin,
                "trade_date": trade_date,
                "units": units,
                "yield_rate": yield_rate,
                "clean_price": clean_price,
                "face_value": result["face_value"],
                "coupon_rate": result["coupon_rate"],
                "maturity_date": result["maturity_date"]
            }
        
        except Exception as e:
            return {"error": f"Error calculating clean price: {str(e)}"}
    
    def _calculate_accrued_interest(self, isin, calculation_date):
        """
        Calculate accrued interest for a bond
        
        Args:
            isin (str): ISIN of the bond
            calculation_date (datetime): Date for calculation
        
        Returns:
            float: Accrued interest
        """
        try:
            # Get cashflows
            cashflows = self.data_loader.get_cashflows_by_isin(isin)
            if cashflows.empty:
                return 0
            
            # Convert calculation date to datetime if it's not already
            if not isinstance(calculation_date, datetime):
                calculation_date = pd.to_datetime(calculation_date)
            
            # Find the most recent coupon date before calculation date
            past_cashflows = cashflows[pd.to_datetime(cashflows['cash_flow_date']) <= calculation_date]
            
            if past_cashflows.empty:
                # If no past cashflows, use the first future cashflow and assume it's the first coupon
                future_cashflows = cashflows[pd.to_datetime(cashflows['cash_flow_date']) > calculation_date]
                if future_cashflows.empty:
                    return 0
                
                next_coupon_date = pd.to_datetime(future_cashflows['cash_flow_date'].min())
                next_coupon_amount = float(future_cashflows.loc[future_cashflows['cash_flow_date'] == next_coupon_date.strftime('%Y-%m-%d'), 'interest_amount'].iloc[0])
                
                # Assume coupon frequency is semi-annual (182 days) or annual (365 days)
                # Check if there's another coupon within a year
                next_year = next_coupon_date + timedelta(days=365)
                next_year_cashflows = future_cashflows[pd.to_datetime(future_cashflows['cash_flow_date']) < next_year]
                
                if len(next_year_cashflows) > 1:
                    # Semi-annual coupon
                    coupon_period = 182
                else:
                    # Annual coupon
                    coupon_period = 365
                
                # Calculate days accrued (negative since we're before the first coupon)
                days_accrued = (calculation_date - (next_coupon_date - timedelta(days=coupon_period))).days
                
                # Calculate accrued interest
                accrued_interest = (next_coupon_amount * days_accrued) / coupon_period
                
                return max(0, accrued_interest)
            
            # Find the last coupon date
            last_coupon_date = pd.to_datetime(past_cashflows['cash_flow_date'].max())
            
            # Find the next coupon date
            future_cashflows = cashflows[pd.to_datetime(cashflows['cash_flow_date']) > calculation_date]
            if future_cashflows.empty:
                return 0
            
            next_coupon_date = pd.to_datetime(future_cashflows['cash_flow_date'].min())
            next_coupon_amount = float(future_cashflows.loc[future_cashflows['cash_flow_date'] == next_coupon_date.strftime('%Y-%m-%d'), 'interest_amount'].iloc[0])
            
            # Calculate days in coupon period
            coupon_period_days = (next_coupon_date - last_coupon_date).days
            
            # Calculate days accrued
            days_accrued = (calculation_date - last_coupon_date).days
            
            # Calculate accrued interest
            accrued_interest = (next_coupon_amount * days_accrued) / coupon_period_days
            
            return accrued_interest
        
        except Exception as e:
            print(f"Error calculating accrued interest: {str(e)}")
            return 0 