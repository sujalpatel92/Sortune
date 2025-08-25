# Agent Onboarding: Sortune Repository

Welcome, fellow AI! This document is your guide to understanding and contributing to the **Sortune** repository.

## 1. Project Overview

**Sortune** is an AI-assisted YouTube Music playlist manager. Its goal is to provide tools to curate, sort, and re-title playlists using a combination of a web API, a background worker, and a user interface.

- **Tech Stack**: Python 3.12, FastAPI, Streamlit, RQ, Redis, Docker.
- **Package Manager**: `uv`.

## 2. Repository Structure

This is a Python monorepo. It's crucial to understand the layout:

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
├─ scripts/                # Helper scripts
├─ tests/                  # Unit + integration tests
├─ .github/                # CI/CD workflows and issue templates
├─ AGENT_ONBOARDING.md     # This file!
├─ Makefile                # Common development commands
├─ pyproject.toml          # ROOT project: for dev tooling ONLY
└─ README.md
```

**Key Architectural Principles**:

- **Monorepo Separation**: Code is separated into `apps` (runnable applications) and `packages` (sharable libraries).
- **Dependency Management**:
    - Each app and package in `apps/` and `packages/` has its **own** `pyproject.toml` for its specific dependencies.
    - The **root `pyproject.toml`** is ONLY for development tools (`ruff`, `mypy`, `pytest`, etc.). **Do not add application or library dependencies here.**
- **Editable Installs**: The development setup uses `pip install -e` for all local apps and packages, so changes are reflected immediately.

## 3. Development Workflow

The `scripts/dev.sh` script and the `Makefile` are your primary tools for development. The `Makefile` is slightly more comprehensive.

**Common Commands**:

- `make install`: Install all dependencies and local packages.
- `make api`: Run the FastAPI server locally.
- `make ui`: Run the Streamlit UI locally.
- `make worker`: Run the RQ worker.
- `make dev-up`: Start the entire application stack using Docker Compose.
- `make dev-down`: Stop the Docker Compose stack.

## 4. Testing and Quality

Before submitting any changes, you **must** run the quality checks.

- `make test`: Run `pytest` for all unit and integration tests.
- `make fmt`: Format the code with `ruff`.
- `make typecheck`: Run `mypy` for static type analysis.
- `scripts/dev.sh all`: A convenient script to run `fmt`, `typecheck`, and `test` in one command.

## 5. Key Entry Points

- **API**: `apps/api/sortune_api/main.py`
- **UI**: `apps/ui/streamlit_app/app.py`
- **Worker Jobs**: Defined in `apps/worker/sortune_worker/jobs/`. See `demo.py` for an example.

## 6. Important "Don'ts" & Guidelines

- **Do Not Edit Build Artifacts**: Never directly edit files in `dist/`, `build/`, or similar directories. Always modify the source files.
- **Respect the Monorepo Structure**: When adding a new dependency for the API, add it to `apps/api/pyproject.toml`, not the root `pyproject.toml`.
- **Run Checks Before Committing**: Always run `make fmt` and `make test` to ensure your changes are clean and don't break anything.
- **Use the Makefile Guards**: The `Makefile` has `guard-*` targets (`guard-main`, `guard-clean`, `guard-synced`). These are used in the `release` process to prevent common mistakes. Be aware of their purpose.
- **YouTube Music Adapter is a Stub**: The current `YTMusicClient` in `packages/adapters/` only returns sample data. A real implementation is a future task. Do not assume it connects to the live YouTube Music service.
- **Environment Variables**: Configuration is managed via environment variables. A `.env.example` file is provided in the root. When running with Docker, this is copied to `.env`.

By following these guidelines, you'll be a productive and effective contributor to the Sortune project. Happy coding!
