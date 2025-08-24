# ---------- Base image ----------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_SYSTEM_PYTHON=1 \
    PROJECT_ROOT=/app

WORKDIR /app

# OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git \
    && rm -rf /var/lib/apt/lists/*

# uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# ---------- Copy sources ----------
COPY packages ./packages
COPY apps/worker ./apps/worker
COPY pyproject.toml ./pyproject.toml

# ---------- Install dependencies ----------
RUN uv pip install -e packages/core -e packages/adapters --system \
    && uv pip install -e apps/worker --system

# ---------- Runtime ----------
# Launch an RQ worker connected to Redis
CMD ["python", "-c", "\
    from rq import Worker, Connection; \
    from redis import Redis; \
    import os; \
    r = Redis.from_url(os.getenv('REDIS_URL','redis://redis:6379/0')); \
    with Connection(r): Worker(['default']).work()"]
