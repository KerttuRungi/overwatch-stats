import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
api_url = "https://overfast-api.tekrop.fr"

class GeneralStatsResponse(BaseModel):
    time_played: int
    games_won: int
    games_lost: int
    winrate: float
    
class PlayerStatsSummaryResponse(BaseModel):
    general: GeneralStatsResponse
    # heroes: list[str] # add listing top 3 heros, getting py playtime from api

@router.get("/players/{battle_tag}/stats/summary")
async def get_player_stats_summary(battle_tag: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/players/{battle_tag}/stats/summary")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()
        )
    return PlayerStatsSummaryResponse(**response.json())
