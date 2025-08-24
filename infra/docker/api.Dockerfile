# ---------- Base image ----------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_SYSTEM_PYTHON=1 \
    PROJECT_ROOT=/app

WORKDIR /app

# OS deps (add gcc/musl-dev if you compile wheels later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git \
    && rm -rf /var/lib/apt/lists/*

# uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# ---------- Copy sources ----------
# Copy only what we need for the API container
COPY packages ./packages
COPY apps/api ./apps/api
COPY pyproject.toml ./pyproject.toml

# ---------- Install dependencies ----------
# Editable installs for local dev; uv installs into system site-packages
RUN uv pip install -e packages/core -e packages/adapters -e packages/ai --system \
    && uv pip install -e apps/api --system

# ---------- Runtime ----------
EXPOSE 8000
CMD ["uvicorn", "sortune_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
