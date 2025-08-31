# Agent Onboarding: Sortune Repository

Welcome, fellow AI (and humans)! This guide helps you understand and contribute to **Sortune** efficiently.

## 1) What this project is

**Sortune** is an AI-assisted YouTube Music playlist manager. It helps curate, sort, and re-title playlists via:

* **FastAPI** backend (`apps/api`)
* **RQ** worker for background jobs (`apps/worker`)
* **Streamlit** demo UI (`apps/ui`)

**Stack**: Python 3.12, FastAPI, Streamlit, RQ, Redis, Docker.
**Package manager**: `uv`.

> If present, agents should first read `repo_state.json` (machine) and `REPO_STATE.md` (human) for a live snapshot of files, CI, and tags.

## 2) Repo structure (monorepo)

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
├─ scripts/                # Helper scripts (dev.sh, seed, etc.)
├─ tests/                  # Unit + integration tests
├─ .github/                # CI/CD workflows and issue templates
├─ Makefile                # Common developer commands
├─ pyproject.toml          # Root: dev tooling ONLY (ruff/mypy/pytest)
└─ README.md               # Quickstart, architecture
```

**Principles**

* Keep runnable **apps** and reusable **packages** separate.
* Use a `src/` layout for Python packages/apps (e.g., `apps/api/src/sortune_api`).
* Each subproject has its **own** `pyproject.toml`.
  The **root** `pyproject.toml` is **tooling only**—don’t add app/package deps there.
* Dev uses editable installs with `uv` (`uv pip install -e …`) so code changes reflect immediately.
* The `uv.lock` lockfile is committed; after dependency changes, run `uv lock` at repo root and commit the update.

## 3) First 5 minutes (local dev)

```bash
# 1) Install dev deps + local packages
make install

# 2) Start Redis (Docker) in one terminal
scripts/dev.sh redis

# 3) Seed a demo playlist into Redis
REDIS_URL=redis://localhost:6379/0 scripts/dev.sh seed

# 4) Run API and UI in separate terminals
scripts/dev.sh api
scripts/dev.sh ui
# Open: API docs → http://localhost:8000/docs
#       UI → http://localhost:8501  (use playlist id "demo"); try AI suggestions expander
```

**Docker dev stack**

```bash
cp .env.example .env
scripts/dev.sh up   # brings up API, UI, Worker, Redis
scripts/dev.sh down
```

## 4) Commands you’ll use a lot

* `make install` — install dev deps + local packages
* `make api` / `make ui` / `make worker` — run services locally
* `make fmt` — ruff format & lint fixes
* `make typecheck` — mypy
* `make test` — pytest (unit + integration)
* `make dev-up` / `make dev-down` — compose up/down
* `uv lock` — refresh `uv.lock` after dependency changes; commit the lockfile

## 5) Versioning & releases (important for agents)

* The project uses **tags** (`vX.Y.Z`) and **setuptools-scm** to derive versions.
* The Makefile exports `SETUPTOOLS_SCM_PRETEND_VERSION` from the latest tag so builds are consistent locally and in CI.

Example snippet used by the Makefile:

```make
TAG := $(shell git describe --tags --abbrev=0 2>/dev/null || echo v0.0.0)
VERSION := $(patsubst v%,%,$(TAG))
export SETUPTOOLS_SCM_PRETEND_VERSION := $(VERSION)
```

**CI/CD** (GitHub Actions)

* `ci.yml` runs lint, typecheck, tests.
* `publish-release.yml` creates a CHANGELOG PR for a given tag on `main`.
* `release-from-tag.yml` builds a release when a `v*.*.*` tag is pushed (and enforces “tag is on main”).

## 6) Key entry points

* API: `apps/api/src/sortune_api/main.py`
* UI: `apps/ui/streamlit_app/app.py`
* AI: `packages/ai/src/sortune_ai/` (BaseLLM, providers, prompts, schemas)
* Worker jobs: `apps/worker/src/sortune_worker/jobs/` (see `demo.py`)

## 7) Important do’s and don’ts

* **Do** add dependencies to the **specific app/package** `pyproject.toml`.
  **Don’t** add runtime deps to the root `pyproject.toml`.
* **Do** run `make fmt`, `make typecheck`, and `make test` before proposing changes.
* **Do** use **Conventional Commits** (e.g., `feat:`, `fix:`, `chore:`) to keep release notes clean.
* **Don’t** assume the **YouTube Music adapter** is live: it’s a **stub** today; real `ytmusicapi` integration is a TODO.
* **Don’t** read or commit real secrets: use `.env.example`. `.env` is git-ignored by policy.

### AI / LLM config (when testing AI features)
Set the following env vars, or add them to `.env`:

```bash
OPENAI_API_KEY=sk-...
SORTUNE_LLM_PROVIDER=langchain
SORTUNE_LLM_BACKEND=openai
SORTUNE_LLM_MODEL=gpt-4o-mini
SORTUNE_LLM_TEMPERATURE=0.6
# Optional deterministic seed
# SORTUNE_LLM_SEED=42
```

API endpoint for suggestions: `POST /ai/suggest-playlist-names`

## 8) Current limitations & near-term tasks

* YT Music client is a **stub** → integrate `ytmusicapi` and map to `packages/core` models.
* Add more **playlist rules** (artist diversity, freshness, tempo/energy proxies).
* Hook up **LLM title generator** from `packages/ai/prompts`.
* Optional persistence upgrade to Postgres (see `ROADMAP.md`).

## 9) Agent checklist (follow this order)

1. If available, load `repo_state.json` + `REPO_STATE.md` for context.
2. Never read `.env`; reference `.env.example` for variable names.
3. For dependency changes, edit the **relevant subproject** `pyproject.toml`.
4. Implement or modify code under `apps/*` or `packages/*` as appropriate.
5. Run `make fmt && make typecheck && make test` locally.
6. Propose a PR with **Conventional Commit** message and brief rationale.
7. If release-worthy, tag `vX.Y.Z` on `main` (maintainers only) to trigger the release flow.

---

By following this onboarding, both AIs and humans can make safe, fast, high-quality changes to Sortune. Happy hacking!
