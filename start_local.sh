#!/usr/bin/env sh
set -e
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
set -a
. ./.env
set +a
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
