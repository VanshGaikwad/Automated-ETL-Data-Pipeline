"""
Data transformation module - Cleaning, enrichment, and business logic
"""

import pandas as pd
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

from .validators import validate_column_presence, validate_data_types

def transform_data(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """
    Apply all transformation rules to data
    
    Args:
        df: Raw DataFrame
        table_name: Name of table for applying specific rules
    
    Returns:
        Transformed DataFrame
    """
    try:
        logger.info(f"Starting transformation for {table_name} table")
        
        # Step 1: Validate columns exist
        validate_column_presence(df, table_name)
        
        # Step 2: Clean data
        df = clean_data(df)
        
        # Step 3: Apply table-specific transformations
        if table_name == "customers":
            df = transform_customers(df)
        elif table_name == "orders":
            df = transform_orders(df)
        
        # Step 4: Validate types after transformation
        validate_data_types(df, table_name)
        
        logger.info(f"✓ Transformation complete for {table_name}. Shape: {df.shape}")
        return df
    
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning
    
    Args:
        df: Raw DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    try:
        logger.info("Cleaning data...")
        
        # Remove leading/trailing whitespace
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
        
        # Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        dropped = initial_rows - len(df)
        
        if dropped > 0:
            logger.info(f"Dropped {dropped} duplicate rows")
        
        logger.info("✓ Data cleaning complete")
        return df
    
    except Exception as e:
        logger.error(f"Error in data cleaning: {str(e)}")
        raise

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Customer-specific transformations
    
    Args:
        df: Customers DataFrame
    
    Returns:
        Transformed customers DataFrame
    """
    try:
        logger.info("Applying customer transformations...")
        
        # Standardize email to lowercase
        df['email'] = df['email'].str.lower()
        
        # Parse registration date
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        
        # Add derived columns
        df['registration_year'] = df['registration_date'].dt.year
        df['account_age_days'] = (datetime.now() - df['registration_date']).dt.days
        
        # Standardize country names
        df['country'] = df['country'].str.upper()
        
        logger.info("✓ Customer transformations applied")
        return df
    
    except Exception as e:
        logger.error(f"Error in customer transformation: {str(e)}")
        raise

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Order-specific transformations
    
    Args:
        df: Orders DataFrame
    
    Returns:
        Transformed orders DataFrame
    """
    try:
        logger.info("Applying order transformations...")
        
        # Parse dates
        df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Add derived metrics
        df['amount_category'] = pd.cut(df['amount'], 
                                       bins=[0, 50, 100, 500, float('inf')],
                                       labels=['small', 'medium', 'large', 'enterprise'])
        
        # Standardize status
        df['status'] = df['status'].str.upper()
        
        # Remove negative amounts
        df = df[df['amount'] >= 0]
        
        # Add processing date
        df['processed_date'] = datetime.now()
        
        logger.info("✓ Order transformations applied")
        return df
    
    except Exception as e:
        logger.error(f"Error in order transformation: {str(e)}")
        raise

def aggregate_data(df: pd.DataFrame, group_by: list, agg_config: Dict[str, str]) -> pd.DataFrame:
    """
    Aggregate data based on grouping columns
    
    Args:
        df: DataFrame to aggregate
        group_by: Columns to group by
        agg_config: Aggregation configuration
    
    Returns:
        Aggregated DataFrame
    """
    try:
        logger.info(f"Aggregating data by {group_by}...")
        
        aggregated = df.groupby(group_by).agg(agg_config).reset_index()
        
        logger.info(f"✓ Aggregated to {len(aggregated)} rows")
        return aggregated
    
    except Exception as e:
        logger.error(f"Error in aggregation: {str(e)}")
        raise
