"""
Unit tests for ETL pipeline components
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors import extract_from_s3
from src.transformers import transform_data, clean_data
from src.validators import validate_column_presence, check_null_values, check_duplicates
from src.loaders import save_to_csv

class TestExtractors:
    """Test data extraction"""
    
    def test_extract_customers(self):
        """Test extracting customer data"""
        df = extract_from_s3('customers.csv')
        assert not df.empty
        assert 'customer_id' in df.columns
        assert len(df) > 0
    
    def test_extract_orders(self):
        """Test extracting order data"""
        df = extract_from_s3('orders.csv')
        assert not df.empty
        assert 'order_id' in df.columns

class TestValidators:
    """Test data validation"""
    
    def test_column_presence(self):
        """Test required columns validation"""
        df = extract_from_s3('customers.csv')
        assert validate_column_presence(df, 'customers')
    
    def test_null_values(self):
        """Test null value detection"""
        df = extract_from_s3('customers.csv')
        nulls = check_null_values(df)
        assert isinstance(nulls, dict)
    
    def test_duplicates(self):
        """Test duplicate detection"""
        df = extract_from_s3('customers.csv')
        dups = check_duplicates(df, ['customer_id'])
        assert isinstance(dups, int)

class TestTransformers:
    """Test data transformation"""
    
    def test_clean_data(self):
        """Test data cleaning"""
        df = pd.DataFrame({
            'name': ['  John  ', '  Jane  '],
            'email': ['john@test.com', 'jane@test.com']
        })
        df_clean = clean_data(df)
        assert df_clean['name'].iloc[0] == 'John'
    
    def test_transform_customers(self):
        """Test customer transformation"""
        df = extract_from_s3('customers.csv')
        df_transformed = transform_data(df, 'customers')
        assert 'email' in df_transformed.columns
        assert df_transformed['email'].iloc[0].islower()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
