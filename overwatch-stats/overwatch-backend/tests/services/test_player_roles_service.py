from models.player import Players
from schemas import HeroStats, PlayerStatsData, RoleStats
from services.player_roles_service import build_role_profile, main_role, top_heroes_for_role

ROLE_MAP = {"ana": "support", "mercy": "support", "kiriko": "support", "lucio": "support", "tracer": "damage"}


def hero(name, time_played):
    return HeroStats(hero=name, games_played=1, games_won=1, time_played=time_played, winrate=50.0)


def role(time_played):
    return RoleStats(games_played=1, games_won=1, time_played=time_played, winrate=50.0)


def player():
    return Players(username="Ana-1", avatar="a.png", namecard="n.png")


def test_main_role_is_the_one_with_most_hours():
    assert main_role({"tank": 1.0, "damage": 5.0, "support": 3.0}) == "damage"


def test_main_role_is_none_without_playtime():
    assert main_role({}) is None
    assert main_role({"tank": 0}) is None


def test_top_heroes_for_role_only_keeps_that_role_by_time_played():
    heroes = [hero("tracer", 900), hero("mercy", 100), hero("ana", 300), hero("kiriko", 200), hero("lucio", 50)]

    top = top_heroes_for_role(heroes, "support", ROLE_MAP, count=3)

    assert [h.hero for h in top] == ["ana", "kiriko", "mercy"]


def test_top_heroes_for_role_ignores_heroes_missing_from_the_map():
    assert top_heroes_for_role([hero("new-hero", 100)], "support", ROLE_MAP) == []


def test_build_role_profile():
    result = PlayerStatsData(
        heroes=[hero("tracer", 900), hero("ana", 300)],
        roles={"damage": role(3600), "support": role(36000)},
    )

    profile = build_role_profile(player(), result, ROLE_MAP)

    assert profile.main_role == "support"
    assert profile.role_hours == {"damage": 1.0, "support": 10.0}
    assert [h.hero for h in profile.top_heroes] == ["ana"]
    assert profile.error is None


def test_build_role_profile_reports_error_message():
    profile = build_role_profile(player(), "Stats unavailable (404).", ROLE_MAP)

    assert profile.main_role is None
    assert profile.error == "Stats unavailable (404)."


def test_build_role_profile_without_roles_is_an_error():
    profile = build_role_profile(player(), PlayerStatsData(), ROLE_MAP)

    assert profile.main_role is None
    assert profile.error is not None
