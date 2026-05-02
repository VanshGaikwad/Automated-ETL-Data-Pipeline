# Automated ETL Data Pipeline

This project is an ETL pipeline I built to show how raw CSV data can be ingested, validated, transformed, and loaded into a warehouse-like database. It simulates AWS S3 locally with files in `data/raw/`, uses Pandas for transformation and validation, and writes the final output to SQLite locally. The Airflow DAG is included to show how the same workflow would be orchestrated in production, and the loader has a Snowflake-ready branch for future cloud setup.

## What this project does

The pipeline processes two sample datasets: `customers.csv` and `orders.csv`.

1. Extracts raw data from the local S3-like folder `data/raw/`.
2. Validates the data with schema checks, null checks, duplicate checks, and type checks.
3. Transforms the data with Pandas, for example by cleaning text, parsing dates, normalizing values, and creating derived columns.
4. Loads the cleaned data into a local SQLite database so the full pipeline can run on a laptop.
5. Orchestrates the workflow with Apache Airflow through `dags/etl_pipeline_dag.py`.

## Why I built it this way

- It shows a complete ETL flow instead of a single script.
- It includes validation before loading, which is important in real data engineering work.
- It has a modular code structure with separate extract, validate, transform, and load layers.
- It includes Airflow orchestration, logging, and unit tests.
- It can run locally without AWS or Snowflake access, so it is easy to demonstrate on my machine.

## Tech Stack

- Python
- Pandas
- Apache Airflow
- SQLite for the local demo warehouse
- Snowflake-ready loader template for production
- Pydantic-style schema validation

## Project Structure

```
├── dags/
│   └── etl_pipeline_dag.py   # Airflow orchestration
├── src/
│   ├── config.py             # Paths, schemas, rules
│   ├── extractors.py         # Read raw data
│   ├── validators.py         # Schema and quality checks
│   ├── transformers.py       # Cleaning and business rules
│   └── loaders.py            # Load into SQLite or Snowflake
├── data/
│   ├── raw/                  # Sample input data
│   └── processed/            # Output files
├── tests/                    # Basic unit tests
├── demo.py                   # Run the pipeline without Airflow
├── requirements.txt          # Dependencies
└── README.md                 # Project overview
```

## How to run locally

### Fastest option
```bash
cd "d:\50LPA\Automated ETL Data Pipeline"
python demo.py
```

### Airflow option
```bash
cd "d:\50LPA\Automated ETL Data Pipeline"
setup.bat
```

Then start Airflow in two terminals:

```bash
airflow webserver --port 8080
```

```bash
airflow scheduler
```

Open `http://localhost:8080` in your browser.

## Example transformations

- Customers: lowercase emails, parse registration dates, calculate account age, standardize country names.
- Orders: parse order dates, categorize amounts, standardize status values, filter invalid rows.

## Configuration

Edit `src/config.py` if you want to change:

- Input paths
- Validation schemas
- Transformation rules
- SQLite or Snowflake target settings

## Author

Built Mar 2026 - Present
