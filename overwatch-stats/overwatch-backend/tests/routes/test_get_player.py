import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.get_player import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_get_player_returns_summary(client, overfast_api):
    overfast_api.respond(200, {
        "summary": {
            "username": "Tracer",
            "avatar": "https://example.com/avatar.png",
            "namecard": "https://example.com/namecard.png",
            "title": "Cheerful",
            "endorsement": {"level": 3, "frame": "https://example.com/frame.svg"},
            "last_updated_at": 1700000000,
        },
        "stats": {"pc": {}},
    })

    response = client.get("/players/Tracer-1234")

    assert response.status_code == 200
    assert response.json() == {
        "summary": {
            "username": "Tracer",
            "avatar": "https://example.com/avatar.png",
            "namecard": "https://example.com/namecard.png",
        }
    }
    assert overfast_api.requested_urls == ["https://overfast-api.tekrop.fr/players/Tracer-1234"]


def test_get_player_relays_api_error(client, overfast_api):
    overfast_api.respond(404, {"error": "Player not found"})

    response = client.get("/players/Unknown-0000")

    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "Player not found"}}
