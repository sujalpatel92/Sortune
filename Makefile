# Use: `make <target>`
SHELL := /bin/bash
UV ?= uv
PY ?= python
COMPOSE := infra/compose.yaml
BRANCH ?= main
REMOTE ?= origin

.PHONY: install fmt lint typecheck test api worker ui dev-up dev-down clean release changelog guard-main guard-clean guard-synced help

# Show available targets
help:
	@echo "Usage: make <target> [VAR=value]"
	@echo
	@echo "Available targets:"
	@echo "  install      - Install local packages (editable) and app deps"
	@echo "  fmt          - Format code and auto-fix with ruff"
	@echo "  lint         - Lint only (no fixes)"
	@echo "  typecheck    - Run mypy on packages/"
	@echo "  test         - Run pytest"
	@echo "  api          - Start FastAPI with uvicorn (reload)"
	@echo "  worker       - Start RQ worker (requires local Redis)"
	@echo "  ui           - Start Streamlit demo UI"
	@echo "  dev-up       - Docker compose up (build) using $(COMPOSE)"
	@echo "  dev-down     - Docker compose down and remove volumes"
	@echo "  clean        - Remove caches and build artifacts"
	@echo "  release      - Create and push semver tag VERSION=X.Y.Z"
	@echo "  changelog    - Trigger GitHub workflow to update CHANGELOG (TAG=...)"
	@echo "  guard-main   - Ensure you are on BRANCH=$(BRANCH)"
	@echo "  guard-clean  - Ensure working tree is clean"
	@echo "  guard-synced - Ensure no unpushed commits to $(REMOTE)/$(BRANCH)"
	@echo
	@echo "Examples:"
	@echo "  make release VERSION=0.2.0"
	@echo "  make changelog TAG=v0.2.0"

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

guard-main:
	@cur=$$(git rev-parse --abbrev-ref HEAD); \
	if [ "$$cur" != "$(BRANCH)" ]; then \
	  echo "✖ You are on '$$cur'. Switch to '$(BRANCH)'."; exit 1; fi

guard-clean:
	@if ! git diff --quiet || ! git diff --cached --quiet; then \
	  echo "✖ Working tree not clean. Commit or stash changes."; exit 1; fi

guard-synced:
	@git fetch $(REMOTE) $(BRANCH) --tags
	@if git log --oneline $(REMOTE)/$(BRANCH)..HEAD | grep . >/dev/null; then \
	  echo "✖ You have unpushed commits. Push to $(REMOTE)/$(BRANCH) first."; exit 1; fi

# Create & push a semver tag vX.Y.Z (triggers release-from-tag.yml)
release: guard-main guard-clean guard-synced
	@test -n "$(VERSION)" || (echo "Usage: make release VERSION=0.1.0"; exit 1)
	@echo "$(VERSION)" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$$' || \
	  (echo "✖ VERSION must be X.Y.Z"; exit 1)
	@tag="v$(VERSION)"; \
	if git rev-parse "$$tag" >/dev/null 2>&1; then \
	  echo "✖ Tag $$tag already exists."; exit 1; fi; \
	git tag -a "$$tag" -m "$$tag"; \
	git push $(REMOTE) "$$tag"; \
	echo "✅ Pushed $$tag. Release workflow will run shortly."

# Trigger the manual CHANGELOG update workflow (opens a PR)
changelog:
	@test -n "$(TAG)" || (echo "Usage: make changelog TAG=v0.1.0"; exit 1)
	@gh --version >/dev/null 2>&1 || (echo "✖ GitHub CLI not installed or not on PATH"; exit 1)
	# EITHER call by workflow name (as set in the YAML)...
	@gh workflow run "Update CHANGELOG.md via PR (manual)" -f tag=$(TAG) --ref $(BRANCH) || \
	# ...OR by filename if you prefer:
	gh workflow run .github/workflows/publish-release.yml -f tag=$(TAG) --ref $(BRANCH)
	@echo "📝 Requested CHANGELOG PR for $(TAG). Check Actions/PRs."
