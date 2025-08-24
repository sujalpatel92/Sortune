#!/usr/bin/env bash
set -euo pipefail

UV="${UV:-uv}"
PY="${PY:-python}"
COMPOSE_FILE="infra/compose.yaml"
UVRUN="${UV} run --no-project"

usage() {
  cat <<'EOF'
Sortune Dev Helper

Usage:
  scripts/dev.sh <command>

Commands:
  install         Install local editable packages with uv
  seed            Seed demo data into Redis (uses REDIS_URL env or localhost)
  api             Run FastAPI locally on :8000 (requires local deps)
  ui              Run Streamlit UI locally on :8501 (requires local deps)
  redis           Start a local Redis via docker on :6379
  up              docker compose up (API, UI, Worker, Redis)
  down            docker compose down -v
  fmt             Ruff format + fix
  lint            Ruff check (no fix)
  typecheck       Mypy type checking
  test            Run pytest
  all             fmt + typecheck + test

Environment:
  UV              uv binary (default: uv)
  PY              python binary (default: python)
  REDIS_URL       Redis URL (default in scripts uses localhost)
EOF
}

cmd_install() {
  echo "==> Installing root development tools (ruff, mypy, etc.)"
  # First, install the dev tools from the root pyproject.toml without a build
  $UV pip compile pyproject.toml --extra dev | $UV pip install -r -

  echo "==> Installing local monorepo packages (editable)"
  # Now, install all your local apps and packages in a single, efficient command
  $UV pip install \
    -e packages/core \
    -e packages/adapters \
    -e packages/ai \
    -e apps/api \
    -e apps/worker

  # UI runs via streamlit; install its deps too:
  $UV pip install streamlit

  echo "==> Done. Your environment is ready."
}

cmd_seed() {
  echo "==> Seeding demo playlist into Redis (${REDIS_URL:-redis://localhost:6379/0})"
  $UVRUN $PY scripts/bootstrap_dev.py
}

cmd_api() {
  echo "==> Starting FastAPI on http://localhost:8000"
  $UVRUN uvicorn sortune_api.main:app --host 0.0.0.0 --port 8000 --reload
}

cmd_ui() {
  echo "==> Starting Streamlit UI on http://localhost:8501"
  $UVRUN streamlit run apps/ui/streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0
}

cmd_redis() {
  echo "==> Launching Redis docker container on :6379"
  docker run --rm -p 6379:6379 redis:7-alpine
}

cmd_up() {
  echo "==> docker compose up (dev stack)"
  docker compose -f "$COMPOSE_FILE" up --build
}

cmd_down() {
  echo "==> docker compose down -v"
  docker compose -f "$COMPOSE_FILE" down -v
}

cmd_fmt() {
  echo "==> Ruff format + fix"
  $UVRUN ruff format .
  $UVRUN ruff check . --fix
}

cmd_lint() {
  echo "==> Ruff lint"
  $UVRUN ruff check .
}

cmd_typecheck() {
  echo "==> mypy on packages/"
  $UVRUN mypy packages/
}

cmd_test() {
  echo "==> pytest"
  $UVRUN pytest -q
}

cmd_all() {
  cmd_fmt
  cmd_typecheck
  cmd_test
}

main() {
  local cmd="${1:-}"
  case "$cmd" in
    install)    cmd_install ;;
    seed)       cmd_seed ;;
    api)        cmd_api ;;
    ui)         cmd_ui ;;
    redis)      cmd_redis ;;
    up)         cmd_up ;;
    down)       cmd_down ;;
    fmt)        cmd_fmt ;;
    lint)       cmd_lint ;;
    typecheck)  cmd_typecheck ;;
    test)       cmd_test ;;
    all)        cmd_all ;;
    ""|help|-h|--help) usage ;;
    *) echo "Unknown command: $cmd"; echo; usage; exit 1 ;;
  esac
}

main "$@"
