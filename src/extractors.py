"""
Data extraction module - Reading from S3 (simulated locally) and other sources
"""

import pandas as pd
import json
from pathlib import Path
from typing import Union, List
import logging

logger = logging.getLogger(__name__)

from .config import DATA_RAW, S3_CONFIG

def extract_from_s3(source_path: str, file_type: str = "csv") -> pd.DataFrame:
    """
    Extract data from simulated S3 bucket (local data/raw directory)
    
    Args:
        source_path: Path to source file
        file_type: Type of file ('csv' or 'json')
    
    Returns:
        DataFrame with extracted data
    """
    try:
        full_path = DATA_RAW / source_path
        
        logger.info(f"Extracting data from: {full_path}")
        
        if file_type == "csv":
            df = pd.read_csv(full_path)
        elif file_type == "json":
            df = pd.read_json(full_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        logger.info(f"Successfully extracted {len(df)} rows from {source_path}")
        return df
    
    except FileNotFoundError:
        logger.error(f"Source file not found: {full_path}")
        raise
    except Exception as e:
        logger.error(f"Error extracting data: {str(e)}")
        raise

def extract_batch_files(source_dir: str, file_pattern: str = "*.csv") -> pd.DataFrame:
    """
    Extract and combine multiple files from S3 prefix
    
    Args:
        source_dir: Directory path in S3
        file_pattern: File pattern to match
    
    Returns:
        Combined DataFrame
    """
    try:
        source_path = DATA_RAW / source_dir
        files = list(source_path.glob(file_pattern))
        
        if not files:
            raise FileNotFoundError(f"No files matching {file_pattern} in {source_dir}")
        
        dfs = []
        for file in files:
            logger.info(f"Processing file: {file.name}")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined {len(files)} files into {len(combined_df)} rows")
        return combined_df
    
    except Exception as e:
        logger.error(f"Error in batch extraction: {str(e)}")
        raise
