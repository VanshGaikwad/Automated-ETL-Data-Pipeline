"""
Configuration module for ETL Pipeline
"""

from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# Database configuration
DATABASE_CONFIG = {
    "type": "sqlite",  # Change to "snowflake" for production
    "path": str(PROJECT_ROOT / "data" / "warehouse.db"),
    # For Snowflake production:
    # "account": "your_account",
    # "warehouse": "your_warehouse",
    # "database": "your_database",
    # "user": "your_user",
}

# S3 configuration (simulated locally in data/raw)
S3_CONFIG = {
    "use_local": True,  # Set to False for real AWS S3
    "bucket": "etl-data",
    "region": "us-east-1",
}

# Schema definitions
class CustomerSchema(BaseModel):
    customer_id: int
    customer_name: str
    email: str
    registration_date: str
    country: str

class OrderSchema(BaseModel):
    order_id: int
    customer_id: int
    order_date: str
    amount: float
    status: str

SCHEMAS = {
    "customers": CustomerSchema,
    "orders": OrderSchema,
}

# Transformation rules
TRANSFORMATION_RULES = {
    "customers": {
        "required_columns": ["customer_id", "customer_name", "email", "registration_date", "country"],
        "data_types": {
            "customer_id": "int64",
            "customer_name": "object",
            "email": "object",
            "registration_date": "object",
            "country": "object",
        }
    },
    "orders": {
        "required_columns": ["order_id", "customer_id", "order_date", "amount", "status"],
        "data_types": {
            "order_id": "int64",
            "customer_id": "int64",
            "order_date": "object",
            "amount": "float64",
            "status": "object",
        }
    }
}

# Airflow configuration
AIRFLOW_CONFIG = {
    "dag_id": "etl_data_pipeline",
    "schedule_interval": "@daily",
    "catchup": False,
    "max_active_runs": 1,
}
