import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from database import get_session
from models.hero import Heroes
from models.player import Players
from models.player_stats import PlayerStats
from routes.get_team_compatibility import router


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
    return player


HEROES = [
    {"key": "ana", "name": "Ana", "role": "support"},
    {"key": "tracer", "name": "Tracer", "role": "damage"},
    {"key": "reinhardt", "name": "Reinhardt", "role": "tank"},
]

SUMMARY = {
    "general": {"games_played": 10, "games_won": 5, "games_lost": 5, "time_played": 72000, "winrate": 50.0},
    "heroes": {
        "ana": {"games_played": 8, "games_won": 4, "time_played": 50000, "winrate": 50.0},
        "tracer": {"games_played": 2, "games_won": 1, "time_played": 22000, "winrate": 50.0},
    },
    "roles": {
        "support": {"games_played": 8, "games_won": 4, "time_played": 50000, "winrate": 50.0},
        "damage": {"games_played": 2, "games_won": 1, "time_played": 22000, "winrate": 50.0},
        "tank": None,
    },
}


def test_team_compatibility(client, session, overfast_api):
    add_player(session, "Ana-1234")
    overfast_api.respond(200, SUMMARY)
    overfast_api.respond_to_path("/heroes", 200, HEROES)

    response = client.get("/players/comparison-list/team-compatibility")

    assert response.status_code == 200
    body = response.json()
    [player] = body["players"]
    assert player["main_role"] == "support"
    assert [hero["hero"] for hero in player["top_heroes"]] == ["ana"]
    assert body["assignments"][0]["assigned_role"] == "support"
    assert body["open_slots"] == ["tank", "damage", "damage", "support"]
    assert body["compatible"] is True
    assert session.exec(select(PlayerStats)).all() == []


def test_heroes_are_fetched_once_and_stored(client, session, overfast_api):
    add_player(session, "Ana-1234")
    overfast_api.respond(200, SUMMARY)
    overfast_api.respond_to_path("/heroes", 200, HEROES)

    client.get("/players/comparison-list/team-compatibility")
    client.get("/players/comparison-list/team-compatibility")

    hero_requests = [url for url in overfast_api.requested_urls if url.endswith("/heroes")]
    assert len(hero_requests) == 1
    assert {hero.key for hero in session.exec(select(Heroes)).all()} == {"ana", "tracer", "reinhardt"}


def test_player_upstream_failure_is_reported_not_raised(client, session, overfast_api):
    add_player(session, "Unknown-0000")
    overfast_api.respond(404, {"error": "Player not found"})
    overfast_api.respond_to_path("/heroes", 200, HEROES)

    response = client.get("/players/comparison-list/team-compatibility")

    assert response.status_code == 200
    body = response.json()
    assert body["players"][0]["error"] == "Stats unavailable (404)."
    assert body["assignments"] == []
    assert body["compatible"] is False
