from __future__ import annotations

import json
import threading
from http.client import HTTPConnection

import pytest

from ai_todo import __version__
from ai_todo.api.server import create_http_server


@pytest.fixture
def api_server(tmp_path):
    server = create_http_server(host="127.0.0.1", port=0, project_root=tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def _request_json(port: int, path: str = "/api/version") -> tuple[int, dict[str, object], str]:
    connection = HTTPConnection("127.0.0.1", port, timeout=5)
    connection.request("GET", path)
    response = connection.getresponse()
    body = response.read().decode("utf-8")
    connection.close()
    return response.status, json.loads(body), response.getheader("Content-Type") or ""


def test_version_endpoint_returns_app_metadata(api_server):
    status, payload, content_type = _request_json(api_server.server_address[1])

    assert status == 200
    assert content_type == "application/json; charset=utf-8"
    assert payload == {"app_name": "ai-todo", "version": __version__}


def test_version_endpoint_includes_commit_sha_when_available(api_server, monkeypatch):
    monkeypatch.setenv("GIT_COMMIT_SHA", "abc123def456")

    status, payload, _ = _request_json(api_server.server_address[1])

    assert status == 200
    assert payload == {
        "app_name": "ai-todo",
        "version": __version__,
        "commit_sha": "abc123def456",
    }


def test_unknown_route_returns_404(api_server):
    status, payload, _ = _request_json(api_server.server_address[1], "/api/does-not-exist")

    assert status == 404
    assert payload == {"error": "Not found"}
