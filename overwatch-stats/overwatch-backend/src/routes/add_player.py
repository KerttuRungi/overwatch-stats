from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.players_list_repository import PlayersRepository
from services.players_list_service import PlayersService, PlayerProfileSummary

router = APIRouter()

@router.post("/players/add-comparison-list")
async def post_player_profile(player_data: PlayerProfileSummary, session: Session = Depends(get_session)):

    repository = PlayersRepository(session)

    service = PlayersService(repository)

    return service.add_comparison_player(player_data)
