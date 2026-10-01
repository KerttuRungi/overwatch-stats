from schemas import GeneralStats, PlayerStatsComparison
from services.player_stats_service import most_wins, parse_general, top_heroes


def hero(time_played: int) -> dict:
    return {"games_played": 10, "games_won": 5, "games_lost": 5, "time_played": time_played, "winrate": 50.0}


def comparison(username: str, games_won: int | None) -> PlayerStatsComparison:
    general = None
    if games_won is not None:
        general = GeneralStats(games_played=100, games_won=games_won, games_lost=100 - games_won, time_played=1000, winrate=games_won)
    return PlayerStatsComparison(username=username, avatar="", general=general)


def test_top_heroes_sorted_by_time_played_and_limited_to_three():
    data = {"heroes": {"ana": hero(100), "mercy": hero(500), "dva": hero(300), "genji": hero(200)}}

    result = top_heroes(data)

    assert [h.hero for h in result] == ["mercy", "dva", "genji"]


def test_top_heroes_handles_missing_heroes():
    assert top_heroes({"heroes": None}) == []


def test_parse_general_returns_none_for_private_profile():
    assert parse_general({"general": None}) is None
    assert parse_general({}) is None


def test_most_wins_returns_all_tied_players_and_skips_errors():
    players = [comparison("a-1111", 50), comparison("b-2222", 70), comparison("c-3333", 70), comparison("d-4444", None)]

    assert most_wins(players) == ["b-2222", "c-3333"]


def test_most_wins_empty_when_no_stats():
    assert most_wins([comparison("a-1111", None)]) == []
