from models.player import Players
from schemas import HeroStats, PlayerRoleProfile, PlayerStatsData
from services.player_stats_service import TOP_HEROES_COUNT, top_heroes

SECONDS_PER_HOUR = 3600


def main_role(role_hours: dict[str, float]) -> str | None:
    """The role with the most time played, or None when nothing was played."""
    if not role_hours or max(role_hours.values()) <= 0:
        return None
    return max(role_hours, key=role_hours.get)


def top_heroes_for_role(
    heroes: list[HeroStats], role: str, role_map: dict[str, str], count: int = TOP_HEROES_COUNT
) -> list[HeroStats]:
    return top_heroes([hero for hero in heroes if role_map.get(hero.hero) == role], count)


def build_role_profile(player: Players, result: PlayerStatsData | str, role_map: dict[str, str]) -> PlayerRoleProfile:
    profile = PlayerRoleProfile(username=player.username, avatar=player.avatar)

    if isinstance(result, str):
        profile.error = result
        return profile

    profile.role_hours = {role: stats.time_played / SECONDS_PER_HOUR for role, stats in result.roles.items()}
    profile.main_role = main_role(profile.role_hours)
    if profile.main_role is None:
        profile.error = "No role data available, the profile may be private."
        return profile

    profile.top_heroes = top_heroes_for_role(result.heroes, profile.main_role, role_map)
    return profile
