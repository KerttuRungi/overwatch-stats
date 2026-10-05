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

    def respond(self, status_code: int, body: dict):
        self.status_code = status_code
        self.body = body

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requested_urls.append(str(request.url))
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
