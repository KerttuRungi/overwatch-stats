import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from schemas import  PlayerProfileSummary

router = APIRouter()
api_url = "https://overfast-api.tekrop.fr"

class PlayerProfileResponse(BaseModel):
    summary: PlayerProfileSummary

@router.get("/players/{battle_tag}")
async def get_player_stats(battle_tag: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/players/{battle_tag}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()
        )

    return PlayerProfileResponse(**response.json())
