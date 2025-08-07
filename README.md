# multipass-experimental-api

This repository contains a FastAPI application organised with a modern,
ORM-based architecture using SQLAlchemy. The project exposes a simple
user management API and serves a static HTML interface from the same
server.

## Getting started

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn app.main:app --reload
```

The API is available under `/v1/users` while the static UI can be viewed
at `http://<host>:<port>/ui`.

## Configuration

The application reads the `DATABASE_URL` environment variable to connect
to a database. If it is not set, a local SQLite database (`app.db`) is
used.

A `docker-compose.yml` file is provided for optionally running PostgreSQL
and Redis services during development.
