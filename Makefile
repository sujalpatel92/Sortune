# Use: `make <target>`
SHELL := /bin/bash
UV ?= uv
PY ?= python
COMPOSE := infra/compose.yaml

.PHONY: install fmt lint typecheck test api worker ui dev-up dev-down clean

install:
	# Editable installs for local dev
	$(UV) pip install -e packages/core -e packages/adapters -e packages/ai
	$(UV) pip install -e apps/api -e apps/worker
	$(UV) pip install streamlit

fmt:
	# Format and auto-fix
	$(UV) run --no-project ruff format .
	$(UV) run --no-project ruff check . --fix

lint:
	# Lint only (no fixes)
	$(UV) run --no-project ruff check .

typecheck:
	$(UV) run --no-project mypy packages/

test:
	$(UV) run --no-project pytest -q

api:
	# FastAPI (hot reload)
	$(UV) run --no-project uvicorn sortune_api.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	# RQ worker attached to local Redis (ensure Redis is running)
	$(UV) run --no-project $(PY) -c "from rq import Worker, Connection; from redis import Redis; \
r=Redis.from_url('redis://localhost:6379/0'); \
import sys; \
print('Starting worker on default queue...'); \
from rq import Queue; \
with Connection(r): Worker(['default']).work()"

ui:
	# Streamlit demo UI
	$(UV) run --no-project streamlit run apps/ui/streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0

dev-up:
	docker compose -f $(COMPOSE) up --build

dev-down:
	docker compose -f $(COMPOSE) down -v

clean:
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@rm -rf .pytest_cache .mypy_cache .ruff_cache .uv
