@echo off
echo ======================================
echo Dolibarr MCP Installation Fix
echo ======================================
echo.
echo Fixing installation and module paths...
echo.

REM Check if virtual environment exists
if not exist "venv_dolibarr" (
    echo Creating virtual environment...
    python -m venv venv_dolibarr
)

echo Activating virtual environment...
call venv_dolibarr\Scripts\activate

echo Installing package in development mode...
pip install -e .

echo.
echo Testing installation...
python -c "import sys; sys.path.insert(0, 'src'); from dolibarr_mcp import __version__; print(f'Dolibarr MCP version: {__version__}')" 2>NUL
if %errorlevel% neq 0 (
    echo.
    echo Installation check failed. Trying alternative fix...
    
    REM Install requirements directly
    pip install requests python-dotenv mcp
    
    REM Create a simple test
    python -c "import sys; print('Python path:'); [print(f'  {p}') for p in sys.path[:5]]"
    
    echo.
    echo Now testing module import with path fix...
    python mcp_server_launcher.py
) else (
    echo Installation successful!
    echo.
    echo You can now run the server with:
    echo   python -m dolibarr_mcp.dolibarr_mcp_server
    echo OR
    echo   python mcp_server_launcher.py
)

echo.
pause
