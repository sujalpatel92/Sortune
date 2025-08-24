import os

# Redis connection string; in Docker it's "redis://redis:6379/0"
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
