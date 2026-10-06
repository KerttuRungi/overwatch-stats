import asyncio
import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from repositories.player_stats_repository import PlayerStatsRepository
from repositories.players_list_repository import PlayersRepository
from schemas import GeneralStats, HeroStats, PlayerStatsData, StatsComparisonResponse
from services.player_stats_service import PlayerStatsService

load_dotenv()

router = APIRouter()
api_url = os.getenv("OVERFAST_API_URL")

async def get_player_stats_from_overfast(
    client: httpx.AsyncClient, battle_tag: str, general: bool = True, heroes: bool = True
) -> PlayerStatsData:
    try:
        response = await client.get(f"{api_url}/players/{battle_tag}/stats/summary")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach the stats API.")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    data = response.json()
    stats = PlayerStatsData()
    if general and data.get("general"):
        stats.general = GeneralStats(**data["general"])
    if heroes:
        stats.heroes = [HeroStats(hero=hero, **values) for hero, values in (data.get("heroes") or {}).items()]
    return stats


@router.get("/players/comparison-list/stats")
async def get_comparison_stats(session: Session = Depends(get_session)) -> StatsComparisonResponse:

    players_repository = PlayersRepository(session)
    stats_repository = PlayerStatsRepository(session)

    players = players_repository.get_all_players()

    async with httpx.AsyncClient(timeout=30) as client:
        results = await asyncio.gather(
            *(get_player_stats_from_overfast(client, player.username, general=True, heroes=True) for player in players),
            return_exceptions=True,
        )

    service = PlayerStatsService(stats_repository)

    return service.compare(players, [_to_result(result) for result in results])


def _to_result(result: PlayerStatsData | BaseException) -> PlayerStatsData | str:
    """A player's stats, or the error message to show in their place."""
    if isinstance(result, PlayerStatsData):
        return result
    if isinstance(result, HTTPException):
        if result.status_code == 502:
            return "Could not reach the stats API."
        return f"Stats unavailable ({result.status_code})."
    raise result
