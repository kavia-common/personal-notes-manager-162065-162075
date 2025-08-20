# personal-notes-manager-162065-162075

Backend (FastAPI) quickstart:

- Copy env: `cp notes_backend/.env.example notes_backend/.env` and set values.
- Install: `pip install -r notes_backend/requirements.txt`
- Run: `uvicorn src.api.main:app --reload --app-dir notes_backend`
  (from the notes_backend directory, simply run `uvicorn src.api.main:app --reload`)

Docker:
- Build: `docker build -t notes-backend ./notes_backend`
- Run: `docker run --env-file ./notes_backend/.env -p 8000:8000 notes-backend`

OpenAPI:
- Visit `/docs` for interactive API docs.
- To regenerate the openapi.json artifact file run from notes_backend: `python -m src.api.generate_openapi`