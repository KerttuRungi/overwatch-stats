import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.get_player_stats import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_get_player_stats_summary(client, overfast_api):
    overfast_api.respond(200, {
        "general": {
            "games_played": 150,
            "games_won": 80,
            "games_lost": 70,
            "time_played": 360000,
            "winrate": 53.33,
            "kda": 2.5,
            "total": {"eliminations": 3000},
        },
        "heroes": {},
        "roles": {},
    })

    response = client.get("/players/Tracer-1234/stats/summary")

    assert response.status_code == 200
    assert response.json() == {
        "general": {
            "time_played": 360000,
            "games_won": 80,
            "games_lost": 70,
            "winrate": 53.33,
        }
    }
    assert overfast_api.requested_urls == [
        "https://overfast-api.tekrop.fr/players/Tracer-1234/stats/summary"
    ]


def test_get_player_stats_summary_error(client, overfast_api):
    overfast_api.respond(404, {"error": "Player not found"})

    response = client.get("/players/Unknown-0000/stats/summary")

    assert response.status_code == 404
    assert response.json() == {"detail": {"error": "Player not found"}}
