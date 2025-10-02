@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Determine script dir
SET SCRIPT_DIR=%~dp0
SET TOOLS_DIR=%SCRIPT_DIR%
SET VENV_DIR=%TOOLS_DIR%\.venv
SET REQ=%TOOLS_DIR%\requirements.txt

:: Create venv if missing
IF NOT EXIST "%VENV_DIR%\Scripts\python.exe" (
    python -m venv "%VENV_DIR%"
)

:: Use the venv python to install requirements and run
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
"%VENV_DIR%\Scripts\pip.exe" install -r "%REQ%"

:: Run the CLI with all args
"%VENV_DIR%\Scripts\python.exe" "%TOOLS_DIR%\devtools.py" %*
