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
│  ├─ api/                 # FastAPI service (package under src/)
│  ├─ worker/              # RQ worker (package under src/)
│  └─ ui/                  # Streamlit demo UI
├─ packages/
│  ├─ core/                # Domain models, services, rules (under src/)
│  ├─ adapters/            # Integrations (Redis, YT Music) (under src/)
│  └─ ai/                  # Prompts, schemas, LLM utilities (under src/)
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

* Each Python package/app uses a `src/` layout (e.g., `apps/api/src/sortune_api`).
* Each **subproject** (apps/api, apps/worker, apps/ui, packages/\*) has its own `pyproject.toml`.
* The **root `pyproject.toml`** is tooling-only (`ruff`, `mypy`, `pytest`, etc.).
* The `uv.lock` lockfile is committed. After changing dependencies, run `uv lock` at the repo root and commit the updated lock.

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

4. (Optional) Enable AI name suggestions

   Set your OpenAI key and LLM config in `.env` (see `.env.example`):

   ```bash
   export OPENAI_API_KEY=sk-...
   export SORTUNE_LLM_PROVIDER=langchain
   export SORTUNE_LLM_BACKEND=openai
   export SORTUNE_LLM_MODEL=gpt-4o-mini
   export SORTUNE_LLM_TEMPERATURE=0.6
   # Optional deterministic seed
   # export SORTUNE_LLM_SEED=42
   ```

5. **Run API and UI (in separate terminals)**

   ```bash
   scripts/dev.sh api
   scripts/dev.sh ui
   ```

6. Open:

   * API docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* UI → [http://localhost:8501](http://localhost:8501)
  - Use playlist ID `demo` → Load → Sort by title
  - Try the expander: “AI — Generate playlist name suggestions”

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

## Lockfile

- File: `uv.lock` is committed for reproducible dependency resolution.
- Refresh after changing any subproject `pyproject.toml` dependencies:

  ```bash
  uv lock
  ```

- Review and commit the updated `uv.lock`.
- CI currently installs via `uv pip` and editable installs; the lockfile supports consistent local/Docker builds.

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
* **AI**: Provider-agnostic LLM layer (BaseLLM), LangChain(OpenAI) provider, prompt templates, schema-constrained generation for playlist naming.
  - Helper: `sortune_ai.generate_playlist_name_suggestions(context, count, seed)`
  - API: `POST /ai/suggest-playlist-names` → returns `PlaylistSuggestions`
  - UI: Streamlit panel to generate suggestions
* **API**: FastAPI app exposing `/health`, `/playlists/{id}`, `/playlists/{id}/sort`
* **Worker**: RQ worker running jobs (e.g., demo seeding)
* **UI**: Streamlit app to load/sort playlists interactively

---

## Status

✅ Skeleton repo is complete: API, Worker, UI, Core, Adapters, AI packages, infra, dev scripts, tests.
✅ LLM-based playlist naming integrated (provider abstraction, env config, API + UI).
⚠️ Next steps:

* Flesh out real **YT Music adapter** with [ytmusicapi](https://github.com/sigma67/ytmusicapi)
* Add more **rules** (artist diversity, freshness, tempo)
* Persist to Postgres (optional)

---

## License

This project is licensed under the [MIT License](./LICENSE).

---
