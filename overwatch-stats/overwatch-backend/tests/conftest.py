import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("OVERFAST_API_URL", "https://overfast-api.tekrop.fr")

import httpx
import pytest


class FakeOverfastApi:
    def __init__(self):
        self.status_code = 200
        self.body = {}
        self.requested_urls = []
        self.path_responses = {}

    def respond(self, status_code: int, body: dict | list):
        self.status_code = status_code
        self.body = body

    def respond_to_path(self, path: str, status_code: int, body: dict | list):
        """Answer requests whose URL path ends with `path` differently from the default response."""
        self.path_responses[path] = (status_code, body)

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requested_urls.append(str(request.url))
        for path, (status_code, body) in self.path_responses.items():
            if request.url.path.endswith(path):
                return httpx.Response(status_code, json=body)
        return httpx.Response(self.status_code, json=self.body)

@pytest.fixture
def overfast_api(monkeypatch):
    api = FakeOverfastApi()
    real_async_client = httpx.AsyncClient

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: real_async_client(transport=httpx.MockTransport(api.handler)),
    )
    return api
