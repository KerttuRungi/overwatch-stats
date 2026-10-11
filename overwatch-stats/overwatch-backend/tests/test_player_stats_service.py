from schemas import GeneralStats, HeroStats, PlayerStatsComparison
from services.player_stats_service import most_wins, top_heroes


def hero(name: str, time_played: int) -> HeroStats:
    return HeroStats(hero=name, games_played=10, games_won=5, time_played=time_played, winrate=50.0)


def comparison(username: str, games_won: int | None) -> PlayerStatsComparison:
    general = None
    if games_won is not None:
        general = GeneralStats(games_played=100, games_won=games_won, games_lost=100 - games_won, time_played=1000, winrate=games_won)
    return PlayerStatsComparison(username=username, avatar="", general=general)


def test_top_heroes_sorted_by_time_played_and_limited_to_three():
    heroes = [hero("ana", 100), hero("mercy", 500), hero("dva", 300), hero("genji", 200)]

    result = top_heroes(heroes)

    assert [h.hero for h in result] == ["mercy", "dva", "genji"]


def test_top_heroes_handles_no_heroes():
    assert top_heroes([]) == []


def test_most_wins_returns_all_tied_players_and_skips_errors():
    players = [comparison("a-1111", 50), comparison("b-2222", 70), comparison("c-3333", 70), comparison("d-4444", None)]

    assert most_wins(players) == ["b-2222", "c-3333"]


def test_most_wins_empty_when_no_stats():
    assert most_wins([comparison("a-1111", None)]) == []
