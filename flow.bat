@echo off
rem Batch script to generate motor insurance analytics project directories and empty starter files

mkdir data
mkdir data\raw
mkdir data\cleaned
mkdir notebooks
mkdir src
mkdir app
mkdir reports
mkdir tests
mkdir logs

type nul > data\raw\customers.csv
type nul > data\raw\vehicles.csv
type nul > data\raw\policies.csv
type nul > data\raw\claims.csv
type nul > data\raw\payments.csv
type nul > data\cleaned\customers_cleaned.csv
type nul > data\cleaned\vehicles_cleaned.csv
type nul > data\cleaned\policies_cleaned.csv
type nul > data\cleaned\claims_cleaned.csv
type nul > data\cleaned\payments_cleaned.csv
type nul > notebooks\insurance_analysis.ipynb
type nul > src\__init__.py
type nul > src\data_loader.py
type nul > src\validation.py
type nul > src\data_cleaner.py
type nul > src\insurance_analysis.py
type nul > src\visualization.py
type nul > src\insights.py
type nul > src\logger.py
type nul > app\streamlit_app.py
type nul > reports\business_report.md
type nul > tests\test_pipeline.py
type nul > tests\test_analysis.py
type nul > tests\test_validation.py
type nul > logs\pipeline.log
type nul > run_pipeline.py
type nul > requirements.txt
type nul > Dockerfile
type nul > .dockerignore
type nul > .gitignore
type nul > README.md

echo Motor Insurance Analytics project structure created successfully!