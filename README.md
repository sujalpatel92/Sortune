# Sortune

AI-assisted YouTube Music playlist manager. Curate, sort, and re-title playlists with clean,
testable Python packages, a FastAPI backend, a background worker, and a simple Streamlit UI.

> Package manager: **uv** (Python 3.12).  
> Repo style: monorepo with isolated packages and apps.  
> Data/cache: Redis (dev) with optional Postgres later.

---

## Repo layout

```text
Sortune/
├─ apps/
│  ├─ api/
│  │  └─ sortune_api/
│  │      ├─ routes/
│  │      └─ __init__.py
│  ├─ worker/
│  │  └─ sortune_worker/
│  │      ├─ jobs/
│  │      └─ __init__.py
│  └─ ui/
│     └─ streamlit_app/
├─ packages/
│  ├─ core/
│  │  └─ sortune_core/
│  │      ├─ models/
│  │      ├─ repos/
│  │      ├─ services/
│  │      ├─ rules/
│  │      └─ __init__.py
│  ├─ adapters/
│  │  └─ sortune_adapters/
│  │      ├─ ytmusic/
│  │      ├─ storage/
│  │      └─ __init__.py
│  └─ ai/
│     └─ sortune_ai/
│         ├─ prompts/
│         └─ __init__.py
├─ infra/
│  ├─ docker/
│  └─ compose.yaml
├─ scripts/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  └─ e2e/
├─ .gitignore
├─ .env.example
├─ LICENSE
├─ Makefile
├─ pyproject.toml
└─ README.md
```

---

## Prereqs

- Python **3.12**
- **uv** ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/))

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- Docker + Docker Compose (for the dev stack)

---

## Quick start (Docker dev stack)

1. Copy env and edit if needed:

```bash
cp .env.example .env
```

1. Bring up services:

```bash
docker compose -f infra/compose.yaml up --build
```

1. Open:

- API docs → [http://localhost:8000/docs](http://localhost:8000/docs)
- UI (Streamlit) → [http://localhost:8501](http://localhost:8501)

### First demo flow in the UI

- Enter playlist ID: `demo`
- Click **Seed demo** (adds sample tracks)
- Click **Load playlist**
- Click **Sort by title**

---

## Local (non-Docker) dev with uv

> Each subpackage/app is an editable install. Use uv from repo root.

```bash
# Install libs
uv pip install -e packages/core -e packages/adapters -e packages/ai

# API app
uv pip install -e apps/api
uv run uvicorn sortune_api.main:app --reload

# Worker app
uv pip install -e apps/worker
uv run python -c "from rq import Queue, Connection, Worker; \
from redis import Redis; \
r=Redis.from_url('redis://localhost:6379/0'); \
with Connection(r): Worker(['default']).work()"

# UI app
uv pip install -e packages/core -e packages/adapters streamlit
uv run streamlit run apps/ui/streamlit_app/app.py
```

Make sure Redis is running locally:

```bash
docker run -p 6379:6379 redis:7-alpine
```

---

## Environment variables

Defined in `.env.example`:

- `SORTUNE_ENV=dev`
- `REDIS_URL=redis://redis:6379/0` (Docker) or `redis://localhost:6379/0` (local)
- `OPENAI_API_KEY=...` (optional; for future AI chains)
- `DATABASE_URL=postgresql+psycopg://user:pass@host:5432/sortune` (future)

---

## Make targets

```bash
make dev-up        # docker compose up (dev)
make dev-down      # docker compose down -v
make fmt           # ruff format + lint
make typecheck     # mypy on packages
make test          # pytest
```

---

## Testing & quality

### Tests

- `pytest` in `tests/` and package-level tests

  ```bash
  uv run pytest -q
  ```

### Lint/format

- `ruff`

  ```bash
  uv run ruff format .
  uv run ruff check . --fix
  ```

### Typing

- `mypy`

  ```bash
  uv run mypy packages/
  ```

---

## API snapshot

- `GET /health` – health check
- `GET /playlists/{playlist_id}` – fetch (from Redis storage)
- `POST /playlists/{playlist_id}/sort?rule_name=by_title` – apply a simple rule and persist

OpenAPI docs at `/docs`.

---

## Architecture notes

- **Core** (`packages/core`): Pydantic models and pure business logic (easy to test).
- **Adapters** (`packages/adapters`): External systems behind clean interfaces (Redis repo, YT Music client stub).
- **AI** (`packages/ai`): Pydantic schemas for LLM outputs + prompt templates.
- **Apps**: Thin shells that wire the above—REST API, background jobs, simple UI.

This separation lets you swap storage or providers without touching core logic.

---

## Next steps

- Implement the real **YT Music** adapter (ytmusicapi), mapping to `sortune_core` models.
- Add more **rules** (e.g., by artist diversity, freshness, tempo if audio features available).
- Introduce **LLM title suggestions** via `packages/ai` chains.
- Optional: Postgres migrations and richer persistence.

---

## Contributing

Branch from `main`, open PRs with:

- Passing tests (`make test`)
- Lint/format clean (`make fmt`)
- Focused commits and clear descriptions

---

## License

This project is licensed under the [MIT License](./LICENSE).

---
