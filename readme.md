# End-to-End Data Engineering Pipeline

An end-to-end data engineering portfolio project that automates sales data ingestion, storage, transformation, validation, and loading into a SQL Server data warehouse. The project also includes automated tests, CI with GitHub Actions, pipeline logging, and an interactive Streamlit dashboard for sales analytics.

## Project Overview

This project demonstrates how raw sales data can be processed through a complete local data engineering workflow, from extraction to analytics.

The pipeline generates sample sales data, stores raw files in an S3-compatible data lake, retrieves and transforms the data, validates data quality, and loads the results into Microsoft SQL Server for analysis.

## Architecture

```text
Python Data Extraction
         |
         v
    Raw Sales Data
         |
         v
SeaweedFS Object Storage
    (S3-Compatible)
         |
         v
  Download Raw Data
         |
         v
Data Cleaning & Transformation
         |
         v
  Data Quality Validation
         |
         v
 Microsoft SQL Server
    Data Warehouse
         |
         v
 Streamlit Dashboard
    Sales Analytics

Pytest Tests ──> GitHub Actions CI
Pipeline Logging ──> Local Log Files
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data extraction, transformation, automation, and orchestration |
| Microsoft SQL Server | Relational database and data warehouse |
| T-SQL | Table definitions, constraints, and database operations |
| SeaweedFS | Local S3-compatible object storage for raw data |
| Docker | Running object storage in a container |
| Pandas | Data processing, if used in the current implementation |
| Pytest | Automated transformation and data quality tests |
| GitHub Actions | Continuous integration and automated test execution |
| Streamlit | Interactive sales analytics dashboard |
| Boto3 | Communication with S3-compatible object storage |
| PyODBC | Python connectivity to SQL Server |
| Git and GitHub | Version control and source code hosting |

## Pipeline Workflow

1. **Extract:** Generate sample sales records and save the raw data as CSV, alongside extraction metadata.
2. **Store:** Upload the raw CSV and metadata files to SeaweedFS using its S3-compatible API.
3. **Retrieve:** Download the raw sales data from object storage for processing.
4. **Transform:** Clean and validate records, check required fields, reject duplicate order IDs, validate quantities and prices, and calculate total sales amounts.
5. **Load:** Load the cleaned records into Microsoft SQL Server, using database constraints and duplicate-handling logic.
6. **Test:** Run automated Pytest tests to verify transformation behavior and data quality rules.
7. **Visualize:** Explore sales metrics and product performance in an interactive Streamlit dashboard.
8. **Automate:** Use GitHub Actions to run the automated tests on pushes and pull requests.

## Data Quality Checks

The transformation stage includes checks for:

- Missing required columns and values
- Duplicate order IDs
- Invalid or non-positive order IDs
- Invalid quantities and prices
- Empty input files
- Correct calculation of total sales amounts

Invalid records cause validation failures rather than being silently accepted.

## Dashboard

The Streamlit dashboard provides a simple view of the sales warehouse, including:

- Total orders
- Total sales
- Average order value
- Sales by product
- Sales records table
- Data refresh functionality

## Project Structure

```text
data-engineering-project/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── infrastructure/
│   └── minio/
│       └── compose.yaml
├── ingestion/
│   ├── extract_sales.py
│   ├── upload_to_lake.py
│   └── download_from_lake.py
├── scripts/
│   ├── transform_sales.py
│   ├── load_to_sqlserver.py
│   ├── run_pipeline.py
│   └── pipeline_logger.py
├── sql/
├── tests/
│   └── test_transform_sales.py
├── dashboard.py
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The `infrastructure/minio/` directory name is retained from the initial setup, but the current object storage service is SeaweedFS.*

## Prerequisites

- Python 3.10 or later
- Docker Desktop
- Microsoft SQL Server
- SQL Server Management Studio (SSMS)
- The Microsoft ODBC Driver for SQL Server
- Git

## Running Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd data-engineering-project
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your GitHub repository.

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure the requirements file includes the packages used by your implementation, such as `boto3`, `python-dotenv`, `pyodbc`, `streamlit`, and `pytest`.

### 4. Configure environment variables

Create a local `.env` file in the project root. Configure the S3-compatible endpoint, credentials, and bucket name for your local SeaweedFS instance.

Do not commit `.env` or real credentials to GitHub. Use your own local configuration.

### 5. Start object storage

Run Docker Compose from the infrastructure directory:

```powershell
docker compose -f infrastructure/minio/compose.yaml up -d
```

### 6. Configure SQL Server

Create the `SalesWarehouse` database in SQL Server and run the required table creation SQL from the project. Configure the server and connection settings in the SQL loading script and dashboard for your local environment.

### 7. Run the pipeline

From the project root:

```powershell
python scripts/run_pipeline.py
```

The pipeline runs the extraction, storage, retrieval, transformation, and SQL Server loading stages.

### 8. Run automated tests

```powershell
python -m pytest tests -v
```

### 9. Launch the dashboard

```powershell
streamlit run dashboard.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Continuous Integration

GitHub Actions runs the project's automated tests when changes are pushed or pull requests are opened. This helps catch transformation and data quality issues before changes are merged.

## Engineering Concepts Demonstrated

- ETL pipeline development
- Data ingestion and transformation
- Data lake and data warehouse concepts
- S3-compatible object storage
- Relational database design
- Data quality validation
- Automated testing
- Pipeline orchestration and logging
- Continuous integration
- Analytics dashboard development

## Current Scope

This is a local portfolio project using generated sample sales data. It is intended to demonstrate data engineering concepts and does not represent real customer transactions or a production deployment.

## Future Improvements

- Ingest data from a public or authorized API
- Implement incremental data loading
- Add stronger retry and error-recovery mechanisms
- Expand data quality and integration tests
- Add structured pipeline monitoring
- Introduce dimensional modeling and additional analytics

## Author

Created as a hands-on data engineering portfolio project to develop practical skills in Python, SQL Server, ETL pipelines, data quality, and analytics.
