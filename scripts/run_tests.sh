#!/usr/bin/env bash
set -euo pipefail
UV="${UV:-uv}"
PY="${PY:-python}"
UVRUN="${UV} run --no-project"

echo "==> Ruff format & lint"
$UVRUN ruff format .
$UVRUN ruff check . --fix

echo "==> Mypy type check"
$UVRUN mypy packages/

echo "==> Pytest"
$UVRUN pytest -q
