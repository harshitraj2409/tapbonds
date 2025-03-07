import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BONDS_DETAILS_FILE, CASHFLOWS_FILE, COMPANY_INSIGHTS_FILE

class DataLoader:
    """
    Utility class to load and process data from CSV files
    """
    def __init__(self):
        self.bonds_details = None
        self.cashflows = None
        self.company_insights = None
        self.load_data()
    
    def load_data(self):
        """
        Load data from CSV files
        """
        try:
            print(f"Loading bonds details from {BONDS_DETAILS_FILE}")
            self.bonds_details = pd.read_csv(BONDS_DETAILS_FILE)
            print(f"Loaded bonds details with shape: {self.bonds_details.shape}")
            
            print(f"Loading cashflows from {CASHFLOWS_FILE}")
            self.cashflows = pd.read_csv(CASHFLOWS_FILE)
            print(f"Loaded cashflows with shape: {self.cashflows.shape}")
            
            print(f"Loading company insights from {COMPANY_INSIGHTS_FILE}")
            self.company_insights = pd.read_csv(COMPANY_INSIGHTS_FILE)
            print(f"Loaded company insights with shape: {self.company_insights.shape}")
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_bond_by_isin(self, isin):
        """
        Get bond details by ISIN
        """
        if self.bonds_details is None:
            return None
        
        # Convert ISIN to uppercase for case-insensitive matching
        isin = isin.upper()
        
        # Filter bonds by ISIN
        return self.bonds_details[self.bonds_details['isin'].str.upper() == isin]
    
    def get_cashflows_by_isin(self, isin):
        """
        Get cashflows for a bond by ISIN
        """
        if self.cashflows is None:
            return None
        
        # Convert ISIN to uppercase for case-insensitive matching
        isin = isin.upper()
        
        # Filter cashflows by ISIN
        return self.cashflows[self.cashflows['isin'].str.upper() == isin]
    
    def get_company_by_name(self, company_name):
        """
        Get company insights by company name
        """
        if self.company_insights is None:
            return None
        
        # Case-insensitive partial matching for company name
        return self.company_insights[self.company_insights['company_name'].str.contains(company_name, case=False, na=False)]
    
    def get_bonds_by_issuer(self, issuer_name):
        """
        Get bonds by issuer name
        """
        if self.bonds_details is None:
            return None
        
        # Use company_name column instead of issuer_name
        return self.bonds_details[self.bonds_details['company_name'].str.contains(issuer_name, case=False, na=False)]
    
    def filter_bonds(self, filters):
        """
        Filter bonds based on criteria
        
        Args:
            filters (dict): Dictionary of filter criteria
                - coupon_rate_min (float): Minimum coupon rate
                - coupon_rate_max (float): Maximum coupon rate
                - maturity_date_min (str): Minimum maturity date (YYYY-MM-DD)
                - maturity_date_max (str): Maximum maturity date (YYYY-MM-DD)
                - credit_rating (list): List of acceptable credit ratings
                - security_type (str): Type of security (e.g., 'Secured', 'Unsecured')
                - issuer_type (str): Type of issuer (e.g., 'PSU', 'Non-PSU')
                - sector (str): Sector of the issuer
        
        Returns:
            pandas.DataFrame: Filtered bonds
        """
        if self.bonds_details is None:
            return None
        
        filtered_bonds = self.bonds_details.copy()
        
        # Extract coupon rate from coupon_details if needed
        if 'coupon_rate' not in filtered_bonds.columns and 'coupon_details' in filtered_bonds.columns:
            # This is a simplified approach - in a real scenario, you'd need more sophisticated parsing
            filtered_bonds['coupon_rate'] = filtered_bonds['coupon_details'].str.extract(r'(\d+\.?\d*)%').astype(float)
        
        # Apply filters
        if 'coupon_rate_min' in filters and filters['coupon_rate_min'] is not None and 'coupon_rate' in filtered_bonds.columns:
            filtered_bonds = filtered_bonds[filtered_bonds['coupon_rate'] >= filters['coupon_rate_min']]
        
        if 'coupon_rate_max' in filters and filters['coupon_rate_max'] is not None and 'coupon_rate' in filtered_bonds.columns:
            filtered_bonds = filtered_bonds[filtered_bonds['coupon_rate'] <= filters['coupon_rate_max']]
        
        if 'maturity_date_min' in filters and filters['maturity_date_min'] is not None:
            filtered_bonds = filtered_bonds[filtered_bonds['maturity_date'] >= filters['maturity_date_min']]
        
        if 'maturity_date_max' in filters and filters['maturity_date_max'] is not None:
            filtered_bonds = filtered_bonds[filtered_bonds['maturity_date'] <= filters['maturity_date_max']]
        
        if 'credit_rating' in filters and filters['credit_rating'] is not None and 'credit_rating_details' in filtered_bonds.columns:
            # This is a simplified approach - in a real scenario, you'd need more sophisticated parsing
            filtered_bonds = filtered_bonds[filtered_bonds['credit_rating_details'].str.contains('|'.join(filters['credit_rating']), case=False, na=False)]
        
        if 'security_type' in filters and filters['security_type'] is not None and 'instrument_details' in filtered_bonds.columns:
            filtered_bonds = filtered_bonds[filtered_bonds['instrument_details'].str.contains(filters['security_type'], case=False, na=False)]
        
        if 'issuer_type' in filters and filters['issuer_type'] is not None and 'issuer_details' in filtered_bonds.columns:
            filtered_bonds = filtered_bonds[filtered_bonds['issuer_details'].str.contains(filters['issuer_type'], case=False, na=False)]
        
        if 'sector' in filters and filters['sector'] is not None and 'issuer_details' in filtered_bonds.columns:
            filtered_bonds = filtered_bonds[filtered_bonds['issuer_details'].str.contains(filters['sector'], case=False, na=False)]
        
        return filtered_bonds
    
    def get_bonds_maturing_in_year(self, year):
        """
        Get bonds maturing in a specific year
        """
        if self.bonds_details is None:
            return None
        
        # Convert year to string
        year_str = str(year)
        
        # Handle NaN values in maturity_date column
        valid_dates = self.bonds_details['maturity_date'].notna()
        
        # Filter bonds by year in maturity date
        return self.bonds_details[valid_dates & self.bonds_details['maturity_date'].str.startswith(year_str, na=False)]
    
    def get_bonds_by_yield_range(self, min_yield, max_yield):
        """
        Get bonds within a specific yield range
        """
        if self.bonds_details is None:
            return None
        
        # Extract yield from coupon_details if needed
        if 'yield' not in self.bonds_details.columns and 'coupon_details' in self.bonds_details.columns:
            # This is a simplified approach - in a real scenario, you'd need more sophisticated parsing
            self.bonds_details['yield'] = self.bonds_details['coupon_details'].str.extract(r'(\d+\.?\d*)%').astype(float)
        
        if 'yield' not in self.bonds_details.columns:
            return pd.DataFrame()  # Return empty DataFrame if yield column doesn't exist
        
        return self.bonds_details[(self.bonds_details['yield'] >= min_yield) & 
                                 (self.bonds_details['yield'] <= max_yield)]
    
    def get_bonds_by_credit_rating(self, ratings):
        """
        Get bonds with specific credit ratings
        """
        if self.bonds_details is None:
            return None
        
        if isinstance(ratings, str):
            ratings = [ratings]
        
        # Use credit_rating_details column
        if 'credit_rating_details' in self.bonds_details.columns:
            return self.bonds_details[self.bonds_details['credit_rating_details'].str.contains('|'.join(ratings), case=False, na=False)]
        
        return pd.DataFrame()  # Return empty DataFrame if credit_rating column doesn't exist
    
    def get_bonds_by_security_type(self, security_type):
        """
        Get bonds by security type (e.g., 'Secured', 'Unsecured')
        """
        if self.bonds_details is None:
            return None
        
        # Use instrument_details column
        if 'instrument_details' in self.bonds_details.columns:
            return self.bonds_details[self.bonds_details['instrument_details'].str.contains(security_type, case=False, na=False)]
        
        return pd.DataFrame()  # Return empty DataFrame if security_type column doesn't exist 