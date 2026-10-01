from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from repositories.players_list_repository import PlayersRepository
from services.players_list_service import PlayersService

router = APIRouter()

@router.delete("/players/comparison-list/{username}")
async def delete_player_profile(username: str, session: Session = Depends(get_session)):

    repository = PlayersRepository(session)

    service = PlayersService(repository)

    try:
        return service.remove_comparison_player(username)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
