import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from database import get_session
from models.player import Players
from models.player_stats import PlayerStats
from routes.get_player_stats import router


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_session] = lambda: session
    return TestClient(app)


def add_player(session, username):
    player = Players(
        username=username,
        avatar=f"https://example.com/{username}.png",
        namecard="https://example.com/namecard.png",
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


OVERFAST_SUMMARY = {
    "general": {
        "games_played": 150,
        "games_won": 80,
        "games_lost": 70,
        "time_played": 360000,
        "winrate": 53.33,
        "kda": 2.5,
    },
    "heroes": {
        "tracer": {"games_played": 100, "games_won": 55, "time_played": 250000, "winrate": 55.0},
        "genji": {"games_played": 50, "games_won": 25, "time_played": 110000, "winrate": 50.0},
    },
    "roles": {
        "damage": {"games_played": 150, "games_won": 80, "time_played": 360000, "winrate": 53.33},
        "tank": None,
    },
}


def test_comparison_stats(client, session, overfast_api):
    add_player(session, "Tracer-1234")
    overfast_api.respond(200, OVERFAST_SUMMARY)

    response = client.get("/players/comparison-list/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["most_wins"] == ["Tracer-1234"]
    [player] = body["players"]
    assert player["username"] == "Tracer-1234"
    assert player["general"] == {
        "games_played": 150,
        "games_won": 80,
        "games_lost": 70,
        "time_played": 360000,
        "winrate": 53.33,
    }
    assert [hero["hero"] for hero in player["top_heroes"]] == ["tracer", "genji"]
    assert player["error"] is None
    assert overfast_api.requested_urls == [
        "https://overfast-api.tekrop.fr/players/Tracer-1234/stats/summary"
    ]
    assert len(session.exec(select(PlayerStats)).all()) == 1


def test_comparison_stats_reports_upstream_error(client, session, overfast_api):
    add_player(session, "Unknown-0000")
    overfast_api.respond(404, {"error": "Player not found"})

    response = client.get("/players/comparison-list/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["most_wins"] == []
    [player] = body["players"]
    assert player["general"] is None
    assert player["error"] == "Stats unavailable (404)."
    assert session.exec(select(PlayerStats)).all() == []
