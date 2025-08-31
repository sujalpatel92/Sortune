# Repository Guidelines

## Project Structure & Module Organization
- Apps: `apps/api` (FastAPI), `apps/worker` (RQ worker), `apps/ui` (Streamlit).
- Packages: `packages/core`, `packages/adapters`, `packages/ai` (installable Python packages used by apps).
- Tests: `tests/unit`, `tests/integration`, `tests/e2e`.
- Infra: `infra/compose.yaml`, Dockerfiles in `infra/docker/`.
- Scripts/Tools: `scripts/`, `tools/`. Config in `pyproject.toml`.

## Build, Test, and Development Commands
- `make install`: Install dev tooling and local packages via `uv` (editable).
- `make fmt`: Format and auto-fix with Ruff (includes import sorting).
- `make lint`: Lint only (no fixes).
- `make typecheck`: Run mypy on `packages/`.
- `make test`: Run pytest quietly.
- `make api` | `make worker` | `make ui`: Run services locally (requires Redis).
- `make dev-up` | `make dev-down`: Docker Compose dev stack (API, Worker, UI, Redis).

## Coding Style & Naming Conventions
- Python 3.12, line length 100. Use type hints where practical.
- Formatting/Linting: Ruff for format and checks (`make fmt`, `make lint`).
- Typing: mypy configured (non-strict). Keep types in public APIs of packages.
- Naming: `snake_case` for modules/functions, `PascalCase` for classes, `CONSTANT_CASE` for constants.
- Package names follow `sortune_<domain>` (e.g., `sortune_core`).

## Testing Guidelines
- Frameworks: pytest (+ pytest-asyncio). Use `fakeredis` in integration tests when Redis isn’t available.
- Layout: mirror source paths under `tests/` (e.g., `tests/unit/core/...`).
- Naming: files `test_*.py`; functions `test_*`.
- Run: `make test`. Add fixtures in `tests/conftest.py` when shared.

## Commit & Pull Request Guidelines
- Conventional Commits enforced via Commitizen hook. Examples:
  - `feat(api): add playlists endpoint`
  - `fix(worker): handle missing redis url`
- PRs must include: description, linked issues (`Fixes #123`), screenshots/logs, and test evidence (see `.github/pull_request_template.md`).
- CI runs lint, typecheck, tests (see `.github/workflows/ci.yml`). Keep PRs small and focused.

## Security & Configuration Tips
- Config via `.env` (see `.env.example`); app settings use `SORTUNE_` prefix (e.g., `SORTUNE_REDIS_URL=redis://localhost:6379/0`).
- Don’t commit real API keys or OAuth secrets. Use Docker Compose (`make dev-up`) for a reproducible local stack.

### AI / LLM Configuration
- Provider selection via env:
  - `SORTUNE_LLM_PROVIDER=langchain`
  - `SORTUNE_LLM_BACKEND=openai`
  - `SORTUNE_LLM_MODEL=gpt-4o-mini`
  - `SORTUNE_LLM_TEMPERATURE=0.6`
  - Optional: `SORTUNE_LLM_SEED=42`
- Credentials: `OPENAI_API_KEY` must be set for the OpenAI backend.
- Public API: `POST /ai/suggest-playlist-names` returns `PlaylistSuggestions`.
