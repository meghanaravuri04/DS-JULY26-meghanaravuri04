 @echo off
REM Project Directory Initialization Script

mkdir data\raw
mkdir data\cleaned
mkdir notebooks
mkdir src
mkdir app
mkdir reports
mkdir tests

type nul > data\raw\logistics_data.csv
type nul > data\cleaned\logistics_cleaned.csv
type nul > notebooks\logistics_analysis.ipynb
type nul > src\__init__.py
type nul > src\data_loader.py
type nul > src\data_cleaner.py
type nul > src\business_analysis.py
type nul > src\visualization.py
type nul > app\streamlit_app.py
type nul > reports\business_report.md
type nul > tests\test_pipeline.py
type nul > run_pipeline.py
type nul > requirements.txt
type nul > README.md
type nul > .gitignore

echo Logistics Delivery Analytics project structure successfully created!

