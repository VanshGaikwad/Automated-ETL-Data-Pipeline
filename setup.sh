#!/bin/bash
# Setup script for ETL Pipeline

echo "=========================================="
echo "ETL Pipeline Setup"
echo "=========================================="

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize Airflow
echo ""
echo "Initializing Airflow..."
export AIRFLOW_HOME=$(pwd)/airflow_home
airflow db init

# Create Airflow user
echo ""
echo "Creating Airflow admin user..."
echo "Username: admin"
echo "Password: admin"
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run demo: python demo.py"
echo "2. Start Airflow:"
echo "   airflow webserver --port 8080"
echo "   airflow scheduler"
echo "3. Access UI: http://localhost:8080"
echo ""
