@echo off

:: Get the directory where the script is located.
set "SCRIPT_DIR=%~dp0"

:: It's good practice to run Python projects in a virtual environment.
:: This script will look for a 'venv' folder.
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
) else {
    echo WARN: Virtual environment not found. Using system's Python.
    echo It is recommended to create one using 'python -m venv venv'.
}

:: Run the main application.
echo.
echo Launching Personal DJ...
echo.
python "%SCRIPT_DIR%run.py"
    echo Docker not found. Please install Docker Desktop first.
    start https://www.docker.com/products/docker-desktop/
    pause
    exit /b
)

REM Check for Ollama
echo Checking Ollama...
where ollama >nul 2>&1
if %errorLevel% neq 0 (
    echo Ollama not found. Installing...
    curl -L https://ollama.com/download/OllamaSetup.exe -o %TEMP%\OllamaSetup.exe
    start /wait %TEMP%\OllamaSetup.exe /S
    echo Please restart your computer after installation completes.
    pause
    exit /b
)

REM Start the application
echo Starting AI DJ...
cd scripts
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_simple.ps1

pause
