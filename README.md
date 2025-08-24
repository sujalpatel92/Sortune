# Sortune

🎶 **Sortune** is an AI-assisted YouTube Music playlist manager.  
Curate, sort, and re-title playlists with clean, testable Python packages,
a FastAPI backend, a background worker, and a Streamlit UI.

---

## Badges

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
[![CI](https://github.com/sujalpatel92/Sortune/actions/workflows/ci.yml/badge.svg)](https://github.com/sujalpatel92/Sortune/actions)

---

## Repo layout

```text
Sortune/
├─ apps/
│  ├─ api/                 # FastAPI service
│  ├─ worker/              # RQ worker (background jobs)
│  └─ ui/                  # Streamlit demo UI
├─ packages/
│  ├─ core/                # Domain models, services, rules
│  ├─ adapters/            # Integrations (Redis, YT Music)
│  └─ ai/                  # Prompts, schemas, LLM utilities
├─ infra/                  # Dockerfiles + docker compose
├─ scripts/                # Helpers (bootstrap, enqueue, dev.sh)
├─ tests/                  # Unit + integration tests
├─ .gitignore
├─ .env.example
├─ LICENSE
├─ Makefile
├─ pyproject.toml          # Root = meta project for dev tooling only
└─ README.md
```

* Each **subproject** (apps/api, apps/worker, apps/ui, packages/\*) has its own `pyproject.toml`.
* The **root `pyproject.toml`** is tooling-only (`ruff`, `mypy`, `pytest`, etc.).

---

## Prereqs

* Python **3.12**
* [uv](https://docs.astral.sh/uv/) package manager
* Docker + Docker Compose (for the dev stack)
* Redis (local docker or in dev stack)

---

## Quick start (local, no Docker)

1. **Install deps**

   ```bash
   scripts/dev.sh install
   ```

2. **Start Redis**

   ```bash
   scripts/dev.sh redis
   ```

   (runs Redis in foreground on :6379)

3. **Seed demo playlist**

   ```bash
   REDIS_URL=redis://localhost:6379/0 scripts/dev.sh seed
   ```

4. **Run API and UI (in separate terminals)**

   ```bash
   scripts/dev.sh api
   scripts/dev.sh ui
   ```

5. Open:

   * API docs → [http://localhost:8000/docs](http://localhost:8000/docs)
   * UI → [http://localhost:8501](http://localhost:8501) → use playlist ID `demo` → Load → Sort by title

---

## Quick start (Docker dev stack)

```bash
cp .env.example .env
scripts/dev.sh up
```

* API → [http://localhost:8000/docs](http://localhost:8000/docs)
* UI → [http://localhost:8501](http://localhost:8501)
* Worker auto-runs jobs
* Redis → localhost:6379

Tear down:

```bash
scripts/dev.sh down
```

---

## Dev helper

`scripts/dev.sh` bundles common tasks:

```bash
scripts/dev.sh install    # install local pkgs + dev deps
scripts/dev.sh seed       # seed demo playlist into Redis
scripts/dev.sh api        # run FastAPI locally
scripts/dev.sh ui         # run Streamlit UI locally
scripts/dev.sh redis      # run Redis in docker
scripts/dev.sh up         # docker compose up
scripts/dev.sh down       # docker compose down
scripts/dev.sh fmt        # ruff format + fix
scripts/dev.sh typecheck  # mypy
scripts/dev.sh test       # pytest
scripts/dev.sh all        # fmt + typecheck + test
```

---

## Testing & quality

* **Ruff** (lint/format)
* **Mypy** (typing)
* **Pytest** (unit/integration, with fakeredis for adapter tests)

Run all in one shot:

```bash
scripts/dev.sh all
```

---

## Architecture

* **Core**: Pydantic models (`Playlist`, `Track`), rules (`ByTitle`), service layer
* **Adapters**: Redis repo, YT Music client (stub now, real API later)
* **AI**: Pydantic schemas for playlist naming, prompt templates
* **API**: FastAPI app exposing `/health`, `/playlists/{id}`, `/playlists/{id}/sort`
* **Worker**: RQ worker running jobs (e.g., demo seeding)
* **UI**: Streamlit app to load/sort playlists interactively

---

## Status

✅ Skeleton repo is complete: API, Worker, UI, Core, Adapters, AI packages, infra, dev scripts, tests.
⚠️ Next steps:

* Flesh out real **YT Music adapter** with [ytmusicapi](https://github.com/sigma67/ytmusicapi)
* Add more **rules** (artist diversity, freshness, tempo)
* Connect **LLM title generator** from `packages/ai/prompts`
* Persist to Postgres (optional)

---

## License

This project is licensed under the [MIT License](./LICENSE).

---
