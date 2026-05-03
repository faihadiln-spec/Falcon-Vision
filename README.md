# Falcon-Vision
AI-powered vision system integrated with LLM for industrial safety and monitoring

## Docker

The repo now includes a backend-only Docker setup:

```bash
docker compose up --build
```

Service:

- `backend`: runs FastAPI with `python:3.11-slim` on port `8000`

Notes:

- The compose file reads environment variables from the root `.env`.
- The backend image copies the model directories from the repo root (`PPE`, `Fall model`, `Fire Detection`, `Face Recognition`).
- Uploaded files are stored in a named Docker volume.
- Face recognition model cache is stored in a named Docker volume.
- This is intended to sit behind your own `nginx` setup on the server.
