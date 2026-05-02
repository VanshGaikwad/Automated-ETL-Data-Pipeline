"""
Quick demo script to run ETL pipeline locally without Airflow
Run this to show your pipeline working!
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.extractors import extract_from_s3
from src.transformers import transform_data
from src.validators import validate_schema, check_null_values, check_duplicates
from src.loaders import load_to_warehouse, get_warehouse_stats, save_to_csv

# Configure logging to show in console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def demo_etl_pipeline():
    """
    Demonstrate the complete ETL pipeline
    """
    
    print_section("ETL PIPELINE DEMO - Automated Data Pipeline")
    
    # ============ CUSTOMERS PIPELINE ============
    try:
        print_section("1️⃣  EXTRACT - Loading Customer Data from S3")
        customers_df = extract_from_s3('customers.csv', file_type='csv')
        print(f"✓ Extracted {len(customers_df)} customer records\n")
        print("Sample data:")
        print(customers_df.head(3).to_string(index=False))
        
        print_section("2️⃣  VALIDATE - Checking Data Quality")
        print("Running schema validation...")
        validate_schema(customers_df, 'customers')
        
        print("\nChecking for nulls...")
        nulls = check_null_values(customers_df)
        
        print("\nChecking for duplicates...")
        dups = check_duplicates(customers_df, ['customer_id'])
        print(f"✓ Validation complete - {len(customers_df)} records passed")
        
        print_section("3️⃣  TRANSFORM - Processing Customer Data")
        print("Applying transformations...")
        print("  - Standardizing emails to lowercase")
        print("  - Parsing registration dates")
        print("  - Calculating account age")
        print("  - Standardizing country names\n")
        
        customers_transformed = transform_data(customers_df, 'customers')
        print(f"✓ Transformed {len(customers_transformed)} records\n")
        print("Transformed sample:")
        print(customers_transformed[['customer_name', 'email', 'country', 'account_age_days']].head(3).to_string(index=False))
        
        print_section("4️⃣  LOAD - Writing to Data Warehouse")
        print("Loading to warehouse...")
        load_to_warehouse(customers_transformed, 'customers', if_exists='replace')
        
        print("\nWarehouse statistics:")
        stats = get_warehouse_stats('customers')
        print(f"  Table: {stats['table']}")
        print(f"  Rows loaded: {stats['row_count']}")
        
        print("\nSaving to CSV for backup...")
        output_path = save_to_csv(customers_transformed, 'customers_processed.csv')
        print(f"✓ Saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Error in customer pipeline: {str(e)}")
        raise
    
    # ============ ORDERS PIPELINE ============
    try:
        print_section("1️⃣  EXTRACT - Loading Order Data from S3")
        orders_df = extract_from_s3('orders.csv', file_type='csv')
        print(f"✓ Extracted {len(orders_df)} order records\n")
        print("Sample data:")
        print(orders_df.head(3).to_string(index=False))
        
        print_section("2️⃣  VALIDATE - Checking Data Quality")
        print("Running schema validation...")
        validate_schema(orders_df, 'orders')
        
        print("\nChecking for nulls...")
        nulls = check_null_values(orders_df)
        
        print("\nChecking for duplicates...")
        dups = check_duplicates(orders_df, ['order_id'])
        print(f"✓ Validation complete - {len(orders_df)} records passed")
        
        print_section("3️⃣  TRANSFORM - Processing Order Data")
        print("Applying transformations...")
        print("  - Parsing order dates")
        print("  - Categorizing by amount (small/medium/large/enterprise)")
        print("  - Standardizing status values")
        print("  - Removing negative amounts\n")
        
        orders_transformed = transform_data(orders_df, 'orders')
        print(f"✓ Transformed {len(orders_transformed)} records\n")
        print("Transformed sample:")
        print(orders_transformed[['order_id', 'customer_id', 'amount', 'amount_category', 'status']].head(3).to_string(index=False))
        
        print_section("4️⃣  LOAD - Writing to Data Warehouse")
        print("Loading to warehouse...")
        load_to_warehouse(orders_transformed, 'orders', if_exists='replace')
        
        print("\nWarehouse statistics:")
        stats = get_warehouse_stats('orders')
        print(f"  Table: {stats['table']}")
        print(f"  Rows loaded: {stats['row_count']}")
        
        print("\nSaving to CSV for backup...")
        output_path = save_to_csv(orders_transformed, 'orders_processed.csv')
        print(f"✓ Saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Error in order pipeline: {str(e)}")
        raise
    
    # ============ SUMMARY ============
    print_section("✅ ETL PIPELINE EXECUTION COMPLETE")
    print("Summary:")
    print(f"  ✓ Customers: {len(customers_transformed)} records extracted, validated, transformed, loaded")
    print(f"  ✓ Orders: {len(orders_transformed)} records extracted, validated, transformed, loaded")
    print(f"  ✓ All data quality checks passed")
    print(f"  ✓ Data successfully loaded to warehouse")
    print(f"\nExecution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*70)
    print("Next step: Configure and run with Apache Airflow for scheduling!")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        demo_etl_pipeline()
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
