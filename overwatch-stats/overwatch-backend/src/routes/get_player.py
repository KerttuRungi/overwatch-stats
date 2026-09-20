import httpx
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from schemas import  PlayerProfileSummary
from sqlmodel import Session
from database import get_session
from repositories.players_list_repository import PlayersRepository
from services.players_list_service import PlayersService
from schemas import PlayerProfileSummary


router = APIRouter()
api_url = "https://overfast-api.tekrop.fr"

class PlayerProfileResponse(BaseModel):
    summary: PlayerProfileSummary


# get all players added to the comparison list
@router.get("/players/comparison-list")
async def get_player_list(session: Session = Depends(get_session)):
    repository = PlayersRepository(session)
    service = PlayersService(repository)

    return service.get_all_players()


@router.get("/players/{battle_tag}")
async def get_player_stats(battle_tag: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/players/{battle_tag}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()
        )

    return PlayerProfileResponse(**response.json())