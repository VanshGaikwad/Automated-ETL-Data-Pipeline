@echo off
REM Setup script for ETL Pipeline (Windows)

echo.
echo ==========================================
echo ETL Pipeline Setup
echo ==========================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Initialize Airflow
echo.
echo Initializing Airflow...
set AIRFLOW_HOME=%cd%\airflow_home
airflow db init

REM Create Airflow user
echo.
echo Creating Airflow admin user...
echo Username: admin
echo Password: admin
airflow users create ^
    --username admin ^
    --password admin ^
    --firstname Admin ^
    --lastname User ^
    --role Admin ^
    --email admin@example.com

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Run demo: python demo.py
echo 2. Start Airflow:
echo    airflow webserver --port 8080
echo    airflow scheduler
echo 3. Access UI: http://localhost:8080
echo.
