# Falcon Vision Backend

FastAPI + MongoDB backend for Falcon Vision.

For the full project overview, setup notes, and teammate handoff details, start from the root README:

```text
../README.md
```

## Quick start

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/create_indexes.py
uvicorn app.main:app --reload
```

## API docs

- Swagger: `http://127.0.0.1:8000/docs`
- Health: `GET /api/health`

## Main active route groups

- `/api/auth`
- `/api/users`
- `/api/employees`
- `/api/employee-faces`

## Current auth model

Dashboard roles:

- `admin`
- `supervisor`

## Face flow

- upload employee images with `POST /api/employee-faces/upload`
- recognition runs later with `POST /api/employee-faces/recognize`
- uploads save images only and do not run the model

## Postman collection

```text
postman/FalconVision.postman_collection.json
```
