"""
Adapters layer for Sortune.

This package contains integrations with external systems such as:
- YouTube Music API wrappers
- Storage backends (Redis, Postgres in future)
- Telemetry / logging adapters
"""
try:
    from ._version import __version__
except Exception:
    __version__ = "0.0.0"