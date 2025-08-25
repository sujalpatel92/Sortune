# Expose jobs so they can be imported easily, e.g.:
# from sortune_worker.jobs.demo import backfill_demo_playlist
try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"
