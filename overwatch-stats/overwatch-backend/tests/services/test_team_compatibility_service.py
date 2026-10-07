from schemas import PlayerRoleProfile
from services.team_compatibility_service import check_compatibility


def profile(username, **hours):
    main = max(hours, key=hours.get) if hours else None
    return PlayerRoleProfile(username=username, avatar="a.png", main_role=main, role_hours=hours)


def roles_of(response):
    return {a.username: a.assigned_role for a in response.assignments}


def test_perfect_team_is_fully_compatible():
    response = check_compatibility([
        profile("t", tank=50),
        profile("d1", damage=50),
        profile("d2", damage=40),
        profile("s1", support=50),
        profile("s2", support=40),
    ])

    assert response.score == 100
    assert response.compatible
    assert response.open_slots == []
    assert response.warnings == []
    assert response.suggestions == []


def test_three_support_mains_warns_and_suggests_best_flex():
    response = check_compatibility([
        profile("t", tank=50),
        profile("d1", damage=50),
        profile("s1", support=50),
        profile("s2", support=40),
        profile("s3", support=30, damage=24),
    ])

    assert not response.compatible
    assert response.warnings == ["3 players main support, only 2 support slots."]
    assert roles_of(response)["s3"] == "damage"
    [suggestion] = response.suggestions
    assert suggestion.username == "s3"
    assert (suggestion.from_role, suggestion.to_role) == ("support", "damage")
    assert "80%" in suggestion.message
    assert response.score < 100


def test_flex_goes_to_the_player_with_most_hours_in_the_open_role():
    response = check_compatibility([
        profile("t", tank=50),
        profile("d1", damage=50),
        profile("s1", support=50, damage=5),
        profile("s2", support=40, damage=20),
        profile("s3", support=30, damage=25),
    ])

    assert roles_of(response)["s3"] == "damage"
    assert roles_of(response)["s1"] == "support"
    assert roles_of(response)["s2"] == "support"


def test_fewer_than_five_players_reports_open_slots():
    response = check_compatibility([profile("t", tank=50), profile("s1", support=50)])

    assert response.open_slots == ["damage", "damage", "support"]
    assert response.compatible
    assert response.score == 100


def test_more_than_five_players_benches_the_extras():
    response = check_compatibility([
        profile("t", tank=50),
        profile("d1", damage=50),
        profile("d2", damage=40),
        profile("s1", support=50),
        profile("s2", support=40),
        profile("s3", support=10),
    ])

    assert response.substitutes == ["s3"]
    assert len(response.assignments) == 5


def test_players_without_role_data_are_listed_but_not_assigned():
    broken = PlayerRoleProfile(username="x", avatar="a.png", error="Stats unavailable (404).")

    response = check_compatibility([profile("t", tank=50), broken])

    assert [p.username for p in response.players] == ["t", "x"]
    assert list(roles_of(response)) == ["t"]
    assert response.substitutes == []


def test_no_eligible_players():
    response = check_compatibility([])

    assert response.assignments == []
    assert response.score == 0
    assert not response.compatible
