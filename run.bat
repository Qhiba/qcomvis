@echo off
call .env\Scripts\activate
uvicorn app:app --reload --port 8080

if %errorlevel% neq 0 (
    echo ERROR: Run update.bat first to ensure the environment is set up.
)

pause