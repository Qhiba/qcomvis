@echo off
call .env\Scripts\activate
gradio app.py --demo-name=demo

if %errorlevel% neq 0 (
    echo ERROR: Run update.bat first to ensure the environment is set up.
)

pause