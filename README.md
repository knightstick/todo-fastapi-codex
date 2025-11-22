# Todo FastAPI Codex

A minimal FastAPI todo application scaffold managed with Poetry.

## Features
- Async FastAPI app with a simple SQLite database
- CRUD endpoints for todo items (`/todos`)
- Organized modules for configuration, database, models, schemas, CRUD logic, and routing

## Getting Started
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Run the development server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
3. Open the interactive docs at `http://127.0.0.1:8000/docs`.

## Project Layout
```
app/
  api/routes/     # FastAPI routers
  core/           # Configuration
  crud/           # CRUD helpers
  models/         # SQLAlchemy table definitions
  schemas/        # Pydantic models
  main.py         # FastAPI application entrypoint
```
