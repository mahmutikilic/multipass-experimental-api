# multipass-experimental-api

This project exposes a simple REST API to manage [Multipass](https://multipass.run/) instances.
It is built with **FastAPI** and Python 3.11, providing both backend logic and a minimal web
interface from a single application.

Run the development server with:

```bash
python app.py
```

or by calling `uvicorn` directly.

The UI is available at `http://<host>:<port>/ui` after starting the server.
