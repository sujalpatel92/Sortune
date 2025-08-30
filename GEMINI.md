# Project Overview

This project, **Sortune**, is an AI-assisted YouTube Music playlist manager. It's a Python-based monorepo that includes a FastAPI backend, a Streamlit user interface, and an RQ worker for background jobs. The architecture is modular, with separate packages for core domain logic, external service adapters (like Redis and YouTube Music), and AI-powered features.

**Key Technologies:**

*   **Backend:** FastAPI
*   **Frontend:** Streamlit
*   **Background Jobs:** RQ (Redis Queue)
*   **Caching/Storage:** Redis
*   **Dependency Management:** uv
*   **Code Quality:** Ruff (linting/formatting), Mypy (type checking)
*   **Testing:** Pytest

# Building and Running

The `scripts/dev.sh` script is the primary entry point for all development tasks.

**Installation:**

To install all dependencies for the project, run:

```bash
scripts/dev.sh install
```

**Running the Application (Docker):**

The easiest way to run the full application stack (API, UI, worker, and Redis) is with Docker Compose:

```bash
cp .env.example .env
scripts/dev.sh up
```

This will start the following services:

*   **API:** `http://localhost:8000`
*   **UI:** `http://localhost:8501`
*   **Redis:** `localhost:6379`

To stop the services, run:

```bash
scripts/dev.sh down
```

**Running Services Individually (Local):**

You can also run each service locally without Docker.

1.  **Start Redis:**

    ```bash
    scripts/dev.sh redis
    ```

2.  **Run the API:**

    ```bash
    scripts/dev.sh api
    ```

3.  **Run the UI:**

    ```bash
    scripts/dev.sh ui
    ```

**Seeding Demo Data:**

To populate Redis with a demo playlist, run:

```bash
scripts/dev.sh seed
```

# Development Conventions

*   **Monorepo Structure:** The project is organized as a monorepo with distinct applications (`apps/*`) and shared packages (`packages/*`).
*   **Testing:** The project uses `pytest` for both unit and integration tests. Tests are located in the `tests/` directory. To run all tests, use:
    ```bash
    scripts/dev.sh test
    ```
*   **Linting and Formatting:** `Ruff` is used for linting and code formatting. To format the code, run:
    ```bash
    scripts/dev.sh fmt
    ```
*   **Type Checking:** `Mypy` is used for static type checking. To run the type checker, use:
    ```bash
    scripts/dev.sh typecheck
    ```
*   **All-in-One Check:** To run formatting, linting, and tests at once, use:
    ```bash
    scripts/dev.sh all
    ```
*   **YouTube Music Integration:** The `YTMusicClient` in `packages/adapters/sortune_adapters/ytmusic/client.py` handles interaction with the YouTube Music API. It requires OAuth credentials, which are configured via environment variables (`.env` file).
*   **AI Integration:** The project uses AI for generating playlist names. The prompt for this is located in `packages/ai/sortune_ai/prompts/name_gen.md`.
