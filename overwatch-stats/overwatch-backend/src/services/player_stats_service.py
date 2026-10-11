from models.player import Players
from models.player_stats import PlayerStats
from repositories.player_stats_repository import PlayerStatsRepository
from schemas import HeroStats, PlayerStatsComparison, PlayerStatsData, StatsComparisonResponse

TOP_HEROES_COUNT = 3


def top_heroes(heroes: list[HeroStats], count: int = TOP_HEROES_COUNT) -> list[HeroStats]:
    return sorted(heroes, key=lambda hero: hero.time_played, reverse=True)[:count]


def most_wins(players: list[PlayerStatsComparison]) -> list[str]:
    with_stats = [player for player in players if player.general]
    if not with_stats:
        return []
    best = max(player.general.games_won for player in with_stats)
    return [player.username for player in with_stats if player.general.games_won == best]


class PlayerStatsService:

    def __init__(self, stats_repository: PlayerStatsRepository):
        self.stats_repository = stats_repository

    def compare(self, players: list[Players], results: list[PlayerStatsData | str]) -> StatsComparisonResponse:
        comparisons = [self._build_comparison(player, result) for player, result in zip(players, results)]

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

    def _build_comparison(self, player: Players, result: PlayerStatsData | str) -> PlayerStatsComparison:
        comparison = PlayerStatsComparison(username=player.username, avatar=player.avatar)

        if isinstance(result, str):
            comparison.error = result
            return comparison

        if not result.general:
            comparison.error = "No stats available, the profile may be private."
            return comparison

        comparison.general = result.general
        comparison.top_heroes = top_heroes(result.heroes)
        return comparison
