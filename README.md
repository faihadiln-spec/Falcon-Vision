# Falcon Vision

Falcon Vision is an AI-based industrial safety and monitoring project that we are still actively building.

This repository currently includes:

- `backend/` for the FastAPI backend
- `frontend/` for the web app UI
- `Face Recognition/` for the face-recognition model work
- `PPE/`, `Fall model/`, and `LLM/` for other project model/research work
- `docs/` for project notes and context

## Status

This project is still in progress, so the structure, features, and documentation may continue to change.

## Main Areas

- authentication and role-based access
- employee and user management
- face upload and recognition flow
- live monitoring UI
- PPE, fall detection, and LLM-related research

## Quick Start

Backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

## Note

This README is intentionally kept simple for now while development is ongoing.
