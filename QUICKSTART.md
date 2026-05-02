# QUICK START GUIDE

## 30-Second Setup

### Windows
```bash
setup.bat
python demo.py
```

### Mac/Linux
```bash
bash setup.sh
python demo.py
```

---

## What This Project Demonstrates

This portfolio project showcases a **production-grade ETL pipeline** with:

✅ **End-to-End Data Pipeline**
- Extract: CSV/JSON from S3 (simulated locally)
- Transform: Data cleaning & enrichment with Pandas
- Load: SQLite database (Snowflake ready)
- Validate: Schema & data quality checks

✅ **Enterprise Features**
- Apache Airflow DAG orchestration
- Error handling & retry logic
- Data validation layer (Pydantic)
- Logging & monitoring
- Type hints throughout

✅ **Professional Code Structure**
- Modular architecture (extractors, transformers, validators, loaders)
- Configuration management
- Unit tests
- Documentation

---

## File Structure

```
Automated ETL Data Pipeline/
├── dags/
│   └── etl_pipeline_dag.py          ← Airflow DAG (orchestration)
├── src/
│   ├── config.py                    ← Configuration & schemas
│   ├── extractors.py                ← Read from S3
│   ├── transformers.py              ← Data transformation logic
│   ├── validators.py                ← Schema & quality validation
│   └── loaders.py                   ← Write to warehouse
├── data/
│   ├── raw/
│   │   ├── customers.csv            ← Sample raw data
│   │   └── orders.csv
│   └── processed/                   ← Output directory
├── tests/
│   └── test_pipeline.py             ← Unit tests
├── demo.py                          ← Quick demo script
├── requirements.txt                 ← Dependencies
├── setup.bat / setup.sh             ← Installation
└── README.md                        ← Full documentation
```

---

## Running the Pipeline

### Option 1: Quick Demo (No Airflow Setup)
```bash
python demo.py
```
This runs the complete pipeline in ~2 seconds and shows:
- ✓ Data extraction from CSV
- ✓ Schema validation
- ✓ Data transformation
- ✓ Loading to database
- ✓ Statistics

### Option 2: Full Airflow Setup
```bash
# First time only
setup.bat  # or setup.sh on Mac/Linux

# Start Airflow
airflow webserver --port 8080  # In one terminal
airflow scheduler               # In another terminal

# View at http://localhost:8080
# Login: admin / admin
```

### Option 3: Docker (With Airflow)
```bash
docker-compose up -d
# Access at http://localhost:8080
```

---

## Key Components Explained

### 1. **Extractors** (`src/extractors.py`)
- Reads CSV/JSON from simulated S3 (local `data/raw/`)
- Handles multiple file types
- Returns Pandas DataFrame

```python
df = extract_from_s3('customers.csv')  # 12 customer records
```

### 2. **Validators** (`src/validators.py`)
- Pydantic schema validation
- Duplicate detection
- Null value checking
- Data type validation

```python
validate_schema(df, 'customers')  # Validates against schema
check_duplicates(df, ['customer_id'])  # Find duplicates
```

### 3. **Transformers** (`src/transformers.py`)
- Data cleaning (trim whitespace, remove duplicates)
- Business logic transformations
- Derived column generation
- Type conversions

```python
df_transformed = transform_data(df, 'customers')
# Normalizes emails, parses dates, calculates age
```

### 4. **Loaders** (`src/loaders.py`)
- SQLite database for local development
- Snowflake integration ready
- Statistics tracking

```python
load_to_warehouse(df_transformed, 'customers')
```

### 5. **Airflow DAG** (`dags/etl_pipeline_dag.py`)
- Orchestrates extract → validate → transform → load
- Parallel processing for customers & orders
- Error handling and retries
- Task dependencies visualization

---

## Data Transformations

### Customers Pipeline
- ✓ Email standardization (lowercase)
- ✓ Date parsing
- ✓ Account age calculation
- ✓ Country name standardization

### Orders Pipeline
- ✓ Date parsing
- ✓ Amount categorization (small/medium/large/enterprise)
- ✓ Status standardization
- ✓ Negative value filtering

---

## Testing

```bash
# Run unit tests
pytest tests/test_pipeline.py -v
```

Tests cover:
- Data extraction
- Schema validation
- Data transformation
- Duplicate detection

---

## Sample Output

```
EXTRACT: 12 customer records loaded
VALIDATE: ✓ Schema validation passed
TRANSFORM: Email normalized, dates parsed
LOAD: 12 rows loaded to warehouse
WAREHOUSE STATS: Table=customers, Rows=12
```

---

## Configuration

Edit `src/config.py` to:
- Change database type (SQLite → Snowflake)
- Add Snowflake credentials
- Modify schema definitions
- Update transformation rules

---

## For Recruiters

This project demonstrates:

📊 **Data Engineering Skills**
- ETL pipeline design
- Data validation & quality checks
- Error handling

🐍 **Python Expertise**
- Pandas data manipulation
- Pydantic validation
- Logging & configuration

☁️ **Big Data Tools**
- Apache Airflow orchestration
- AWS S3 integration pattern
- Snowflake-ready architecture

🏗️ **Software Engineering**
- Modular, testable code
- Clean architecture
- Documentation
- Version control ready

---

## Next Steps

1. **Run demo.py** to see the pipeline in action
2. **Explore the code** - each module is well-documented
3. **Try Airflow** - run the DAG and monitor execution
4. **Modify the pipeline** - add new transformations, data sources
5. **Deploy to production** - use the Snowflake configuration

---

## Questions?

See the main README.md for complete documentation.
