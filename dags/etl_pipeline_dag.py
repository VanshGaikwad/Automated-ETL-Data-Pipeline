"""
Airflow DAG for ETL Data Pipeline
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.decorators import apply_defaults
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.extractors import extract_from_s3
from src.transformers import transform_data
from src.validators import validate_schema, check_null_values, check_duplicates
from src.loaders import load_to_warehouse, get_warehouse_stats

logger = logging.getLogger(__name__)

# Default DAG arguments
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'etl_data_pipeline',
    default_args=default_args,
    description='End-to-end ETL pipeline with Pandas, Airflow, and Snowflake',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
)

# Task functions
def extract_customers_task():
    """Extract customer data from S3"""
    try:
        logger.info("=== EXTRACT: Reading customers from S3 ===")
        df = extract_from_s3('customers.csv', file_type='csv')
        logger.info(f"Extracted {len(df)} customer records")
        return {'status': 'success', 'records': len(df)}
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        raise

def extract_orders_task():
    """Extract order data from S3"""
    try:
        logger.info("=== EXTRACT: Reading orders from S3 ===")
        df = extract_from_s3('orders.csv', file_type='csv')
        logger.info(f"Extracted {len(df)} order records")
        return {'status': 'success', 'records': len(df)}
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        raise

def validate_customers_task():
    """Validate customer data schema"""
    try:
        logger.info("=== VALIDATE: Checking customer schema ===")
        df = extract_from_s3('customers.csv', file_type='csv')
        
        # Run validations
        validate_schema(df, 'customers')
        null_check = check_null_values(df)
        dup_check = check_duplicates(df, ['customer_id'])
        
        logger.info("✓ Customer validation passed")
        return {'status': 'success', 'nulls': len(null_check), 'duplicates': dup_check}
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise

def validate_orders_task():
    """Validate order data schema"""
    try:
        logger.info("=== VALIDATE: Checking order schema ===")
        df = extract_from_s3('orders.csv', file_type='csv')
        
        # Run validations
        validate_schema(df, 'orders')
        null_check = check_null_values(df)
        dup_check = check_duplicates(df, ['order_id'])
        
        logger.info("✓ Order validation passed")
        return {'status': 'success', 'nulls': len(null_check), 'duplicates': dup_check}
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise

def transform_customers_task():
    """Transform customer data"""
    try:
        logger.info("=== TRANSFORM: Processing customer data ===")
        df = extract_from_s3('customers.csv', file_type='csv')
        df_transformed = transform_data(df, 'customers')
        logger.info(f"✓ Transformed {len(df_transformed)} customer records")
        return {'status': 'success', 'records': len(df_transformed)}
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise

def transform_orders_task():
    """Transform order data"""
    try:
        logger.info("=== TRANSFORM: Processing order data ===")
        df = extract_from_s3('orders.csv', file_type='csv')
        df_transformed = transform_data(df, 'orders')
        logger.info(f"✓ Transformed {len(df_transformed)} order records")
        return {'status': 'success', 'records': len(df_transformed)}
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise

def load_customers_task():
    """Load customer data to warehouse"""
    try:
        logger.info("=== LOAD: Writing customers to warehouse ===")
        df = extract_from_s3('customers.csv', file_type='csv')
        df_transformed = transform_data(df, 'customers')
        load_to_warehouse(df_transformed, 'customers', if_exists='replace')
        stats = get_warehouse_stats('customers')
        logger.info(f"✓ Loaded customers: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Loading failed: {str(e)}")
        raise

def load_orders_task():
    """Load order data to warehouse"""
    try:
        logger.info("=== LOAD: Writing orders to warehouse ===")
        df = extract_from_s3('orders.csv', file_type='csv')
        df_transformed = transform_data(df, 'orders')
        load_to_warehouse(df_transformed, 'orders', if_exists='replace')
        stats = get_warehouse_stats('orders')
        logger.info(f"✓ Loaded orders: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Loading failed: {str(e)}")
        raise

# Task definitions
extract_customers = PythonOperator(
    task_id='extract_customers',
    python_callable=extract_customers_task,
    dag=dag,
)

extract_orders = PythonOperator(
    task_id='extract_orders',
    python_callable=extract_orders_task,
    dag=dag,
)

validate_customers = PythonOperator(
    task_id='validate_customers',
    python_callable=validate_customers_task,
    dag=dag,
)

validate_orders = PythonOperator(
    task_id='validate_orders',
    python_callable=validate_orders_task,
    dag=dag,
)

transform_customers = PythonOperator(
    task_id='transform_customers',
    python_callable=transform_customers_task,
    dag=dag,
)

transform_orders = PythonOperator(
    task_id='transform_orders',
    python_callable=transform_orders_task,
    dag=dag,
)

load_customers = PythonOperator(
    task_id='load_customers',
    python_callable=load_customers_task,
    dag=dag,
)

load_orders = PythonOperator(
    task_id='load_orders',
    python_callable=load_orders_task,
    dag=dag,
)

# DAG dependencies: Extract -> Validate -> Transform -> Load
extract_customers >> validate_customers >> transform_customers >> load_customers
extract_orders >> validate_orders >> transform_orders >> load_orders
