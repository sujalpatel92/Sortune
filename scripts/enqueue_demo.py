"""
Helper script to enqueue the demo job into the default RQ queue.
Usage:
    uv run python scripts/enqueue_demo.py
"""

from redis import Redis
from rq import Queue
from sortune_worker.jobs.demo import backfill_demo_playlist


def main():
    redis_url = "redis://localhost:6379/0"  # adjust if running in Docker
    r = Redis.from_url(redis_url)
    q = Queue("default", connection=r)

    job = q.enqueue(backfill_demo_playlist)
    print(f"Enqueued job {job.id} to backfill demo playlist")


if __name__ == "__main__":
    main()
