@echo off
:: Dolibarr MCP Setup Script - Fixed Version
:: Handles cleanup of build artifacts before installation

echo.
echo ======================================
echo Dolibarr MCP Development Setup
echo ======================================
echo.

:: Clean up old build artifacts
echo Cleaning up old build artifacts...
if exist "*.egg-info" (
    echo Removing old egg-info directories...
    for /d %%i in (*.egg-info) do (
        echo   Removing %%i
        rmdir /s /q "%%i"
    )
)
if exist "src\*.egg-info" (
    echo Removing src egg-info directories...
    for /d %%i in (src\*.egg-info) do (
        echo   Removing %%i
        rmdir /s /q "%%i"
    )
)
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "__pycache__" rmdir /s /q __pycache__
if exist "src\dolibarr_mcp\__pycache__" rmdir /s /q "src\dolibarr_mcp\__pycache__"

:: Remove old virtual environment if exists
if exist "venv_dolibarr" (
    echo Removing old virtual environment...
    rmdir /s /q venv_dolibarr
)

:: Create new virtual environment
echo.
echo Creating new virtual environment...
python -m venv venv_dolibarr
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in PATH
    pause
    exit /b 1
)

:: Activate and setup
echo.
echo Installing dependencies...
call venv_dolibarr\Scripts\activate.bat

:: Ensure pip is installed and upgraded
python -m ensurepip --upgrade 2>nul
python -m pip install --upgrade pip setuptools wheel

:: Install requirements
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found
)

:: Install package in editable mode
echo.
echo Installing dolibarr-mcp package...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install package
    pause
    exit /b 1
)

:: Create .env from example if not exists
if not exist .env (
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo Please edit .env with your Dolibarr API credentials
    )
)

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Virtual environment: venv_dolibarr
echo.
echo Next steps:
echo 1. Edit .env file with your Dolibarr API credentials
echo 2. Run: venv_dolibarr\Scripts\activate
echo 3. Test: python -m dolibarr_mcp
echo.
pause
