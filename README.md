# multipass-experimental-api

This project exposes a simple REST API to manage [Multipass](https://multipass.run/) instances.
It is built with **FastAPI** and Python 3.11, providing both backend logic and a minimal web
interface from a single application. All API endpoints are served under `/v1/api` and are
protected with JWT authentication backed by Redis.

Run the development server with:

```bash
python app.py
```

or by calling `uvicorn` directly.

The UI is available at `http://<host>:<port>/ui` after starting the server.

### Docker services

A small `docker-compose.yml` file is included to run PostgreSQL and Redis for development:

```bash
docker compose up -d
```

The application itself does not run in Docker but expects these services when authentication is enabled.
