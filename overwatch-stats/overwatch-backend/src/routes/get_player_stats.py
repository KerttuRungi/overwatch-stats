from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.player_stats_repository import PlayerStatsRepository
from repositories.players_list_repository import PlayersRepository
from schemas import StatsComparisonResponse
from services.player_stats_service import PlayerStatsService

router = APIRouter()

@router.get("/players/comparison-list/stats")
async def get_comparison_stats(session: Session = Depends(get_session)) -> StatsComparisonResponse:

    players_repository = PlayersRepository(session)
    stats_repository = PlayerStatsRepository(session)

    service = PlayerStatsService(players_repository, stats_repository)

    return await service.compare_list()
