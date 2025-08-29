@echo off
echo 🚀 Quick Start Dolibarr MCP Server (No Installation Required)
echo.

REM Set UTF-8 encoding for Python
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%cd%\src

REM Check if .env exists
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env 2>nul || (
        echo # Dolibarr MCP Configuration > .env
        echo DOLIBARR_URL=https://your-dolibarr-instance.com/api/index.php >> .env
        echo DOLIBARR_API_KEY=your_api_key_here >> .env
        echo LOG_LEVEL=INFO >> .env
    )
    echo ⚠️  Please edit .env file with your Dolibarr credentials!
    echo    Use: notepad .env
    echo.
    pause
    exit /b 1
)

echo 🔌 Testing connection...
venv_dolibarr\Scripts\python.exe test_connection.py
if errorlevel 1 (
    echo.
    echo ❌ Connection test failed!
    echo 💡 Please check your .env configuration:
    echo    - DOLIBARR_URL should be: https://your-instance.com/api/index.php
    echo    - DOLIBARR_API_KEY should be your valid API key
    echo.
    echo Edit with: notepad .env
    echo.
    pause
    exit /b 1
)

echo.
echo 🎯 Starting Dolibarr MCP Server...
echo 📡 Server will run until you press Ctrl+C
echo.

REM Start the MCP server directly from source
venv_dolibarr\Scripts\python.exe -m dolibarr_mcp.dolibarr_mcp_server

echo.
echo 🛑 Server stopped
pause
