@echo off
echo 🚀 Setting up Dolibarr MCP Development Environment...
echo.

REM Run the setup script
python setup.py

echo.
echo 📋 Quick Start Commands:
echo.
echo   Activate virtual environment:
echo   ^> venv_dolibarr\Scripts\activate
echo.
echo   Test the server:
echo   ^> venv_dolibarr\Scripts\python.exe -m dolibarr_mcp.dolibarr_mcp_server
echo.
echo   Run with Docker:
echo   ^> docker-compose up
echo.

pause
