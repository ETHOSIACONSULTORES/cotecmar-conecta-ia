@echo off
if not exist .venv python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
if not exist .env copy .env.example .env
for /f "usebackq tokens=1,* delims==" %%a in (".env") do set "%%a=%%b"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
