import asyncio
import os
import httpx
from dotenv import load_dotenv

from models.player import Players
from models.player_stats import PlayerStats
from repositories.player_stats_repository import PlayerStatsRepository
from repositories.players_list_repository import PlayersRepository
from schemas import GeneralStats, HeroStats, PlayerStatsComparison, StatsComparisonResponse

load_dotenv()

OVERFAST_API_URL = os.getenv("OVERFAST_API_URL")
TOP_HEROES_COUNT = 3


def parse_general(data: dict) -> GeneralStats | None:
    general = data.get("general")
    if not general:
        return None
    return GeneralStats(**general)


def top_heroes(data: dict, count: int = TOP_HEROES_COUNT) -> list[HeroStats]:
    heroes = data.get("heroes") or {}
    ranked = sorted(heroes.items(), key=lambda item: item[1].get("time_played", 0), reverse=True)
    return [HeroStats(hero=hero, **stats) for hero, stats in ranked[:count]]


def most_wins(players: list[PlayerStatsComparison]) -> list[str]:
    with_stats = [player for player in players if player.general]
    if not with_stats:
        return []
    best = max(player.general.games_won for player in with_stats)
    return [player.username for player in with_stats if player.general.games_won == best]


class PlayerStatsService:

    def __init__(self, players_repository: PlayersRepository, stats_repository: PlayerStatsRepository):
        self.players_repository = players_repository
        self.stats_repository = stats_repository

    async def compare_list(self) -> StatsComparisonResponse:
        players = self.players_repository.get_all_players()

        async with httpx.AsyncClient(timeout=30) as client:
            comparisons = await asyncio.gather(
                *(self._fetch_player_stats(client, player) for player in players)
            )

        snapshots = [
            PlayerStats(
                player_id=player.id,
                **comparison.general.model_dump(),
                top_heroes=[hero.model_dump() for hero in comparison.top_heroes],
            )
            for player, comparison in zip(players, comparisons)
            if comparison.general
        ]
        if snapshots:
            self.stats_repository.add_many(snapshots)

        return StatsComparisonResponse(players=comparisons, most_wins=most_wins(comparisons))

    async def _fetch_player_stats(self, client: httpx.AsyncClient, player: Players) -> PlayerStatsComparison:
        comparison = PlayerStatsComparison(username=player.username, avatar=player.avatar)

        try:
            response = await client.get(f"{OVERFAST_API_URL}/players/{player.username}/stats/summary")
        except httpx.HTTPError:
            comparison.error = "Could not reach the stats API."
            return comparison

        if response.status_code != 200:
            comparison.error = f"Stats unavailable ({response.status_code})."
            return comparison

        data = response.json()
        comparison.general = parse_general(data)
        if not comparison.general:
            comparison.error = "No stats available, the profile may be private."
            return comparison

        comparison.top_heroes = top_heroes(data)
        return comparison
