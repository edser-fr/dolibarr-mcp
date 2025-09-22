@echo off
:: Dolibarr MCP - Clean Build Artifacts
:: Run this before setup if you have installation issues

echo.
echo Cleaning Dolibarr MCP build artifacts...
echo ========================================
echo.

:: Remove all egg-info directories
echo Removing egg-info directories...
for /d %%i in (*.egg-info) do (
    echo   - Removing %%i
    rmdir /s /q "%%i" 2>nul
)
for /d %%i in (src\*.egg-info) do (
    echo   - Removing %%i
    rmdir /s /q "%%i" 2>nul
)
for /d %%i in (src\dolibarr_mcp.egg-info) do (
    echo   - Removing %%i
    rmdir /s /q "%%i" 2>nul
)

:: Remove build directories
if exist build (
    echo Removing build directory...
    rmdir /s /q build
)

if exist dist (
    echo Removing dist directory...
    rmdir /s /q dist
)

:: Remove Python cache
echo Removing Python cache...
for /d /r %%i in (__pycache__) do (
    if exist "%%i" (
        echo   - Removing %%i
        rmdir /s /q "%%i" 2>nul
    )
)

:: Remove .pyc and .pyo files
echo Removing compiled Python files...
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

:: Remove virtual environment
if exist venv_dolibarr (
    echo Removing virtual environment...
    rmdir /s /q venv_dolibarr
)

echo.
echo Cleanup complete!
echo You can now run setup.bat for a fresh installation.
echo.
pause
