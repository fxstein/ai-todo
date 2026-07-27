"""Minimal HTTP API server for ai-todo."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import ClassVar
from urllib.parse import urlparse

from ai_todo.core.version_info import get_version_info


class APIRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for ai-todo API routes."""

    project_root: ClassVar[Path] = Path.cwd()
    server_version = "ai-todo-api/1.0"
    sys_version = ""

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        path = urlparse(self.path).path
        if path == "/api/version":
            self._send_json(HTTPStatus.OK, get_version_info(self.project_root).to_dict())
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def _send_json(self, status: HTTPStatus, payload: dict[str, str]) -> None:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - stdlib override
        return


def _handler_for_project_root(project_root: str | Path | None) -> type[APIRequestHandler]:
    class RequestHandler(APIRequestHandler):
        project_root = Path.cwd()

    RequestHandler.project_root = Path(project_root) if project_root is not None else Path.cwd()
    return RequestHandler


def create_http_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    project_root: str | Path | None = None,
) -> ThreadingHTTPServer:
    """Create an HTTP server exposing the ai-todo API routes."""
    return ThreadingHTTPServer((host, port), _handler_for_project_root(project_root))


def run_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    project_root: str | Path | None = None,
) -> None:
    """Run the ai-todo HTTP API server until interrupted."""
    server = create_http_server(host=host, port=port, project_root=project_root)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
