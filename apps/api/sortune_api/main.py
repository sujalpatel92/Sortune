from fastapi import FastAPI

from .routes import ai as ai_routes
from .routes import playlists

app = FastAPI(
    title="Sortune API",
    version="0.1.0",
    description="API for managing, sorting, and curating YouTube Music playlists",
)

# Routers
app.include_router(playlists.router)
app.include_router(ai_routes.router)


@app.get("/health", tags=["system"])
def health():
    """Simple health check endpoint."""
    return {"status": "ok"}
