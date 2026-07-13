# ⚙️ Automated ETL Data Pipeline

**A production‑style ETL pipeline** that ingests, validates, transforms, and loads raw CSV data into a warehouse‑ready database. Built with **Python, Pandas, Apache Airflow, and SQLite** — with a **Snowflake‑ready** loader for cloud deployment.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Why This Project Matters](#why-this-project-matters)
- [Local Development](#local-development)
- [Configuration](#configuration)
- [Example Transformations](#example-transformations)
- [Author](#author)
- [License](#license)

---

## 🔍 Overview

This project demonstrates a **complete ETL workflow** — from raw CSV ingestion to a structured warehouse database. It simulates a real‑world data engineering environment by:

- **Extracting** data from a local S3‑like folder (`data/raw/`)
- **Validating** data with schema, null, duplicate, and type checks
- **Transforming** data using Pandas (cleaning, parsing, normalising, deriving columns)
- **Loading** the cleaned data into a local **SQLite** database (with a **Snowflake‑ready** branch for production)
- **Orchestrating** the entire pipeline with **Apache Airflow**

The pipeline processes two sample datasets — `customers.csv` and `orders.csv` — making it easy to run and demonstrate on any machine without cloud dependencies.

---

## 🧱 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AIRFLOW DAG (orchestration)                │
│                   dags/etl_pipeline_dag.py                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  EXTRACT  ──►  VALIDATE  ──►  TRANSFORM  ──►  LOAD            │
│  (raw CSV)    (schema/      (Pandas         (SQLite /         │
│   from         quality       cleaning &      Snowflake)        │
│   data/raw/)   checks)       business                         │
│                               rules)                           │
└─────────────────────────────────────────────────────────────────┘
```

The pipeline is **modular** — each stage (extract, validate, transform, load) is isolated in its own Python module, making it testable, maintainable, and extendable.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Modular ETL** | Separate layers for extraction, validation, transformation, and loading — not a single monolithic script. |
| **Data Validation** | Schema checks, null checks, duplicate checks, and type checks before loading (critical for production data quality). |
| **Pandas Transformations** | Text cleaning, date parsing, value normalisation, and derived column creation. |
| **Airflow Orchestration** | Full DAG definition to schedule and monitor the pipeline in production. |
| **Local & Cloud Ready** | Runs locally with SQLite; includes a Snowflake‑ready loader for cloud deployment. |
| **Logging & Testing** | Built‑in logging for observability and unit tests for reliability. |
| **Zero Cloud Dependencies** | Runs entirely on your laptop — perfect for demonstrations and interviews. |

---

## 🛠️ Tech Stack

| Area | Technologies |
|------|--------------|
| **Language** | Python 3.8+ |
| **Data Processing** | Pandas, Pydantic‑style schema validation |
| **Orchestration** | Apache Airflow |
| **Database (Local)** | SQLite |
| **Database (Cloud)** | Snowflake (loader template included) |
| **Testing** | unittest / pytest |
| **Logging** | Python `logging` module |

---

## 📁 Project Structure

```
Automated-ETL-Data-Pipeline/
├── dags/
│   └── etl_pipeline_dag.py      # Airflow DAG definition
├── src/
│   ├── config.py                # Paths, schemas, transformation rules
│   ├── extractors.py            # Read raw data from source
│   ├── validators.py            # Schema and data quality checks
│   ├── transformers.py          # Cleaning and business logic
│   └── loaders.py               # Load into SQLite or Snowflake
├── data/
│   ├── raw/                     # Sample input CSV files
│   └── processed/               # Output files (if any)
├── tests/                       # Unit tests for each module
├── demo.py                      # Run the pipeline without Airflow
├── setup.bat                    # One‑click environment setup (Windows)
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🧠 Why This Project Matters

Recruiters and hiring managers look for **real engineering discipline** — not just code that works, but code that is:

- **Modular** — each responsibility has its own layer
- **Validated** — data quality is checked before loading (prevents garbage‑in, garbage‑out)
- **Orchestrated** — uses Airflow, the industry standard for workflow management
- **Testable** — includes unit tests to catch regressions
- **Cloud‑Ready** — the loader is designed to switch from SQLite to Snowflake with minimal changes

This project demonstrates all of these qualities in a **self‑contained, runnable** package.

---

## 🚀 Local Development

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- (Optional) Apache Airflow installed — or use the `setup.bat` script

### Fastest Option (No Airflow Required)
```bash
cd Automated-ETL-Data-Pipeline
python demo.py
```
This runs the entire pipeline end‑to‑end without Airflow — great for quick testing.

### Airflow Option (Production‑Style)
```bash
cd Automated-ETL-Data-Pipeline
setup.bat
```
Then start Airflow in two separate terminals:
```bash
airflow webserver --port 8080
airflow scheduler
```
Open `http://localhost:8080` in your browser to trigger and monitor the DAG.

---

## ⚙️ Configuration

Edit `src/config.py` to customise:

- **Input / output paths**
- **Validation schemas** (field names, types, required flags)
- **Transformation rules** (cleaning logic, derived columns)
- **Target database settings** (SQLite path or Snowflake connection details)

---

## 📊 Example Transformations

### Customers Dataset
- Lowercase email addresses
- Parse registration dates into datetime objects
- Calculate account age (days since registration)
- Standardise country names (e.g., "USA" → "United States")

### Orders Dataset
- Parse order dates into datetime objects
- Categorise order amounts (e.g., "Low", "Medium", "High")
- Standardise status values (e.g., "shipped" → "Shipped")
- Filter out invalid rows (e.g., orders with negative amounts)

---

## 👤 Author

**Vansh Gaikwad**  
[GitHub](https://github.com/VanshGaikwad)

---

## 📄 License

This project is for demonstration and educational purposes. Contact the author for licensing inquiries.

---

> Built with **Python, Pandas, Airflow, and SQLite** — a complete, production‑ready ETL pipeline from raw data to warehouse.
