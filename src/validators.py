"""
Data validation module - Schema and data quality validation
"""

import pandas as pd
from typing import Any, Dict, List
import logging
from pydantic import ValidationError, BaseModel

logger = logging.getLogger(__name__)

from .config import SCHEMAS, TRANSFORMATION_RULES

def validate_schema(df: pd.DataFrame, table_name: str) -> bool:
    """
    Validate DataFrame against Pydantic schema
    
    Args:
        df: DataFrame to validate
        table_name: Name of the table/schema to validate against
    
    Returns:
        True if valid, raises exception otherwise
    """
    try:
        if table_name not in SCHEMAS:
            raise ValueError(f"Schema not found for table: {table_name}")
        
        schema = SCHEMAS[table_name]
        
        logger.info(f"Validating {len(df)} rows against {table_name} schema")
        
        # Validate each row
        errors = []
        for idx, row in df.iterrows():
            try:
                schema(**row.to_dict())
            except ValidationError as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        if errors:
            logger.warning(f"Schema validation errors found: {len(errors)}")
            for error in errors[:5]:  # Log first 5 errors
                logger.warning(error)
            return False
        
        logger.info(f"✓ Schema validation passed for {table_name}")
        return True
    
    except Exception as e:
        logger.error(f"Error in schema validation: {str(e)}")
        raise

def validate_column_presence(df: pd.DataFrame, table_name: str) -> bool:
    """
    Check if all required columns are present
    
    Args:
        df: DataFrame to check
        table_name: Table name to check against
    
    Returns:
        True if all required columns present
    """
    try:
        rules = TRANSFORMATION_RULES.get(table_name, {})
        required_columns = rules.get("required_columns", [])
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing columns: {missing_columns}")
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"✓ All required columns present for {table_name}")
        return True
    
    except Exception as e:
        logger.error(f"Column validation error: {str(e)}")
        raise

def validate_data_types(df: pd.DataFrame, table_name: str) -> bool:
    """
    Validate column data types
    
    Args:
        df: DataFrame to validate
        table_name: Table name for type mapping
    
    Returns:
        True if types match
    """
    try:
        rules = TRANSFORMATION_RULES.get(table_name, {})
        expected_types = rules.get("data_types", {})
        
        type_mismatches = []
        for col, expected_type in expected_types.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if actual_type != expected_type:
                    type_mismatches.append(f"{col}: expected {expected_type}, got {actual_type}")
        
        if type_mismatches:
            logger.warning(f"Type mismatches: {type_mismatches}")
        else:
            logger.info(f"✓ Data types validated for {table_name}")
        
        return True
    
    except Exception as e:
        logger.error(f"Data type validation error: {str(e)}")
        raise

def check_duplicates(df: pd.DataFrame, key_columns: List[str]) -> int:
    """
    Check for duplicate records
    
    Args:
        df: DataFrame to check
        key_columns: Columns to check for duplicates
    
    Returns:
        Number of duplicates found
    """
    duplicates = df.duplicated(subset=key_columns, keep=False).sum()
    
    if duplicates > 0:
        logger.warning(f"Found {duplicates} duplicate records")
    else:
        logger.info("✓ No duplicates found")
    
    return duplicates

def check_null_values(df: pd.DataFrame) -> Dict[str, int]:
    """
    Check for null/missing values
    
    Args:
        df: DataFrame to check
    
    Returns:
        Dictionary of column -> null count
    """
    null_counts = df.isnull().sum()
    null_columns = null_counts[null_counts > 0].to_dict()
    
    if null_columns:
        logger.warning(f"Null values found: {null_columns}")
    else:
        logger.info("✓ No null values detected")
    
    return null_columns
