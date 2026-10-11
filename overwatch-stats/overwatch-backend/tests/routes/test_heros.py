from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.heros import router

client = TestClient(FastAPI())
client.app.include_router(router)

OVERFAST_HEROES = [
    {"key": "ana", "name": "Ana", "portrait": "https://example.com/ana.png", "role": "support"},
    {"key": "tracer", "name": "Tracer", "portrait": "https://example.com/tracer.png", "role": "damage"},
]


def test_get_heroes_returns_only_key_name_and_role(overfast_api):
    overfast_api.respond(200, OVERFAST_HEROES)

    response = client.get("/heroes")

    assert response.status_code == 200
    assert response.json() == [
        {"key": "ana", "name": "Ana", "role": "support"},
        {"key": "tracer", "name": "Tracer", "role": "damage"},
    ]
    assert overfast_api.requested_urls == ["https://overfast-api.tekrop.fr/heroes"]


def test_get_heroes_relays_upstream_error(overfast_api):
    overfast_api.respond(500, {"error": "boom"})

    response = client.get("/heroes")

    assert response.status_code == 500
    assert response.json() == {"detail": {"error": "boom"}}
