# Infra (Dev Stack)

This folder contains Dockerfiles and a Compose stack for local development.

## Services

- **api** – FastAPI app on **<http://localhost:8000>**
- **ui** – Streamlit demo on **<http://localhost:8501>**
- **worker** – RQ worker consuming the `default` queue
- **redis** – cache/store on **localhost:6379**

## Quick start

```bash
cp .env.example .env
docker compose -f infra/compose.yaml up --build
```

## Live reload & mounts

Compose mounts the repo into each container at `/app` so code changes reflect immediately:

- API uses `uvicorn --reload`
- UI is Streamlit (auto-reload)
- Worker restarts code on next job

## Common commands

```bash
# Start / stop
docker compose -f infra/compose.yaml up --build
docker compose -f infra/compose.yaml down -v

# Tail logs
docker compose -f infra/compose.yaml logs -f api
docker compose -f infra/compose.yaml logs -f worker
docker compose -f infra/compose.yaml logs -f ui
```

## Environment

- `.env` at repo root is loaded by services.
- Defaults use `redis://redis:6379/0` inside Docker; use `redis://localhost:6379/0` when running apps locally.

## Troubleshooting

- **Package not found**: Ensure local packages are installed in containers (Compose build step runs `uv pip install -e ...`). Rebuild:
  `docker compose -f infra/compose.yaml build --no-cache`
- **Port already in use**: Stop conflicting process or change `ports` in `compose.yaml`.
- **No Redis**: Verify the `redis` container is up: `docker ps | grep redis`.

---

### `.dockerignore` (at repo root)

```dockerignore
# Git
.git
.gitignore

# Python build/venv/cache
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.uv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# OS/Editors
.DS_Store
Thumbs.db
.idea/
.vscode/

# Notebooks
.ipynb_checkpoints/
*.ipynb

# Node
node_modules/

# Local data/env
.env
data/
cache/
.cache/
*.parquet
*.sqlite
.streamlit/

# Docs build
docs/_build/
doc/_build/
```
