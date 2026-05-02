"""
Data loader module - Loading transformed data to Snowflake/Database
"""

import pandas as pd
import sqlite3
import logging
from typing import Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)

from .config import DATABASE_CONFIG, DATA_PROCESSED

def load_to_warehouse(df: pd.DataFrame, table_name: str, if_exists: str = "append") -> bool:
    """
    Load transformed data to data warehouse (Snowflake/SQLite)
    
    Args:
        df: DataFrame to load
        table_name: Target table name
        if_exists: How to behave if table exists ('fail', 'replace', 'append')
    
    Returns:
        True if successful
    """
    try:
        logger.info(f"Loading {len(df)} rows to {table_name}...")
        
        if DATABASE_CONFIG["type"] == "sqlite":
            return _load_to_sqlite(df, table_name, if_exists)
        elif DATABASE_CONFIG["type"] == "snowflake":
            return _load_to_snowflake(df, table_name, if_exists)
        else:
            raise ValueError(f"Unsupported database type: {DATABASE_CONFIG['type']}")
    
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def _load_to_sqlite(df: pd.DataFrame, table_name: str, if_exists: str) -> bool:
    """
    Load data to local SQLite database
    
    Args:
        df: DataFrame to load
        table_name: Target table
        if_exists: Behavior if table exists
    
    Returns:
        True if successful
    """
    try:
        db_path = DATABASE_CONFIG["path"]
        
        # Create SQLAlchemy engine
        engine = create_engine(
            f'sqlite:///{db_path}',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool
        )
        
        # Write to database
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        
        logger.info(f"✓ Successfully loaded {len(df)} rows to {table_name}")
        return True
    
    except Exception as e:
        logger.error(f"Error loading to SQLite: {str(e)}")
        raise

def _load_to_snowflake(df: pd.DataFrame, table_name: str, if_exists: str) -> bool:
    """
    Load data to Snowflake (requires snowflake-sqlalchemy)
    
    Args:
        df: DataFrame to load
        table_name: Target table
        if_exists: Behavior if table exists
    
    Returns:
        True if successful
    """
    try:
        # This is a template for Snowflake integration
        # Uncomment and configure when using real Snowflake
        
        # from snowflake.sqlalchemy import URL
        # engine = create_engine(URL(
        #     account=DATABASE_CONFIG["account"],
        #     warehouse=DATABASE_CONFIG["warehouse"],
        #     database=DATABASE_CONFIG["database"],
        #     user=DATABASE_CONFIG["user"],
        # ))
        
        logger.error("Snowflake loading not yet configured")
        raise NotImplementedError("Snowflake configuration required")
    
    except Exception as e:
        logger.error(f"Error loading to Snowflake: {str(e)}")
        raise

def save_to_csv(df: pd.DataFrame, file_name: str) -> str:
    """
    Save processed data to CSV file
    
    Args:
        df: DataFrame to save
        file_name: Output file name
    
    Returns:
        Path to saved file
    """
    try:
        output_path = DATA_PROCESSED / file_name
        df.to_csv(output_path, index=False)
        
        logger.info(f"✓ Saved {len(df)} rows to {output_path}")
        return str(output_path)
    
    except Exception as e:
        logger.error(f"Error saving CSV: {str(e)}")
        raise

def get_warehouse_stats(table_name: str) -> Dict[str, Any]:
    """
    Get statistics from loaded table
    
    Args:
        table_name: Table to analyze
    
    Returns:
        Dictionary with stats
    """
    try:
        if DATABASE_CONFIG["type"] == "sqlite":
            engine = create_engine(
                f'sqlite:///{DATABASE_CONFIG["path"]}',
                connect_args={'check_same_thread': False},
                poolclass=StaticPool
            )
            
            query = f"SELECT COUNT(*) as row_count FROM {table_name}"
            with engine.connect() as conn:
                result = conn.execute(text(query))
                row_count = result.scalar()
            
            stats = {
                "table": table_name,
                "row_count": row_count,
                "status": "loaded"
            }
            
            logger.info(f"Table {table_name} stats: {stats}")
            return stats
        
    except Exception as e:
        logger.error(f"Error getting warehouse stats: {str(e)}")
        raise
