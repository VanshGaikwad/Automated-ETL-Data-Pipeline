# ETL Pipeline Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                            │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │   AWS S3 (CSV)   │  │   AWS S3 (JSON)  │                 │
│  │  customers.csv   │  │   orders.json    │                 │
│  └──────────────────┘  └──────────────────┘                 │
└────────────┬───────────────────────────────────────┬─────────┘
             │                                       │
             └───────────────────┬───────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │         EXTRACTION LAYER                     │
         │  extractors.py                               │
         │  • Read CSV/JSON                             │
         │  • Handle multiple formats                   │
         │  • Error handling                            │
         └───────────────────────┬──────────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │       VALIDATION LAYER                       │
         │  validators.py                               │
         │  • Schema validation (Pydantic)              │
         │  • Null checking                             │
         │  • Duplicate detection                       │
         │  • Data type validation                      │
         └───────────────────────┬──────────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │      TRANSFORMATION LAYER                    │
         │  transformers.py                             │
         │  • Data cleaning                             │
         │  • Business logic                            │
         │  • Derived columns                           │
         │  • Type conversions                          │
         └───────────────────────┬──────────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │        LOADING LAYER                         │
         │  loaders.py                                  │
         │  • SQLite (development)                      │
         │  • Snowflake (production)                    │
         │  • Statistics & monitoring                   │
         └───────────────────────┬──────────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │       DATA WAREHOUSE                         │
         │  ┌──────────────────┐  ┌──────────────────┐ │
         │  │   SQLite (Dev)   │  │ Snowflake (Prod) │ │
         │  │  warehouse.db    │  │  cloud database  │ │
         │  └──────────────────┘  └──────────────────┘ │
         └──────────────────────────────────────────────┘
                                 │
         ┌───────────────────────▼──────────────────────┐
         │     ORCHESTRATION & MONITORING               │
         │  Apache Airflow                              │
         │  • DAG scheduling                            │
         │  • Task dependencies                         │
         │  • Error handling & retries                  │
         │  • SLA tracking                              │
         └──────────────────────────────────────────────┘
```

## Data Flow Pipeline

### Customer Data Pipeline
```
Raw Data (CSV)
    ↓ Extract
12 rows extracted
    ↓ Validate
Schema ✓, Nulls ✓, Duplicates ✓
    ↓ Transform
- Email → lowercase
- Date → parsed
- Account age calculated
- Country → uppercase
    ↓ Load
Warehouse updated
```

### Order Data Pipeline
```
Raw Data (CSV)
    ↓ Extract
20 rows extracted
    ↓ Validate
Schema ✓, Nulls ✓, Duplicates ✓
    ↓ Transform
- Date → parsed
- Amount → categorized
- Status → uppercase
- Negatives removed
    ↓ Load
Warehouse updated
```

## Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                  Airflow DAG                            │
│  (etl_pipeline_dag.py)                                  │
└────────┬──────────────────────────────────────┬─────────┘
         │                                      │
    ┌────▼────────────┐              ┌─────────▼──────┐
    │  Extractors     │              │  Validators    │
    │  (extractors.py)│              │ (validators.py)│
    │                 │              │                │
    │ • extract_*     │              │ • validate_*   │
    │ • read CSV/JSON │              │ • check_*      │
    └────┬────────────┘              └────────┬───────┘
         │                                    │
    ┌────▼──────────────────────────────────▼────┐
    │        Transformers                        │
    │     (transformers.py)                      │
    │                                            │
    │ • transform_data()                         │
    │ • clean_data()                             │
    │ • transform_customers()                    │
    │ • transform_orders()                       │
    └──────────────────┬───────────────────────┘
                       │
         ┌─────────────▼──────────────┐
         │     Loaders                │
         │    (loaders.py)            │
         │                            │
         │ • load_to_warehouse()      │
         │ • _load_to_sqlite()        │
         │ • _load_to_snowflake()     │
         │ • save_to_csv()            │
         │ • get_warehouse_stats()    │
         └─────────────┬──────────────┘
                       │
         ┌─────────────▼──────────────┐
         │   Configuration            │
         │     (config.py)            │
         │                            │
         │ • Paths                    │
         │ • Database config          │
         │ • Schemas                  │
         │ • Rules                    │
         └────────────────────────────┘
```

## Configuration Management

```python
# src/config.py contains:
├── Paths
│   └── PROJECT_ROOT, DATA_RAW, DATA_PROCESSED
├── Database Config
│   ├── type: 'sqlite' or 'snowflake'
│   ├── connection details
│   └── warehouse settings
├── S3 Config
│   ├── use_local: True (dev) / False (prod)
│   ├── bucket name
│   └── region
├── Schema Definitions
│   ├── CustomerSchema (Pydantic model)
│   └── OrderSchema (Pydantic model)
├── Transformation Rules
│   ├── customers: required columns, data types
│   └── orders: required columns, data types
└── Airflow Config
    ├── dag_id
    ├── schedule_interval
    └── retry settings
```

## Error Handling Strategy

```
Pipeline Execution
    ↓
Try Task
    ├─ Success → Next Task
    └─ Failure → 
        ├─ Log Error Details
        ├─ Retry (2x with 5min delay)
        └─ If Failed → Alert & Stop
```

## Data Validation Flow

```
Raw Data
    ↓
1. Column Presence Check
   └─ ✓ All required columns exist?
    ↓
2. Schema Validation (Pydantic)
   └─ ✓ Data types correct?
    ↓
3. Null Value Check
   └─ ✓ No critical nulls?
    ↓
4. Duplicate Detection
   └─ ✓ No duplicate keys?
    ↓
5. Data Type Validation
   └─ ✓ Types match config?
    ↓
✓ Validation Passed → Proceed to Transform
✗ Validation Failed → Alert & Quarantine
```

## Deployment Scenarios

### Development (Local)
```
Data Source: data/raw/*.csv
Validation: Full schema + Pydantic
Transformation: All rules applied
Warehouse: SQLite (warehouse.db)
Orchestration: Manual or local Airflow
```

### Production (Cloud)
```
Data Source: AWS S3 (real buckets)
Validation: Full schema + Pydantic + SLA checks
Transformation: All rules + custom logic
Warehouse: Snowflake (multi-region)
Orchestration: Cloud Airflow / Managed DAGs
Monitoring: CloudWatch + Datadog
```

## Performance Characteristics

| Component | Performance | Notes |
|-----------|-------------|-------|
| Extract | <1s | 32 rows in demo |
| Validate | <1s | Schema + duplicates |
| Transform | <1s | Pandas operations |
| Load | <1s | SQLite insert |
| **Total** | **<5s** | Complete pipeline |

## Security Considerations

```python
# Production checklist:
□ AWS S3 credentials → AWS Secrets Manager
□ Snowflake credentials → AWS Secrets Manager
□ Database encryption → TLS/SSL
□ Data at rest → Encrypted
□ Access control → IAM roles
□ Audit logging → CloudTrail
□ PII handling → Masked in logs
```
