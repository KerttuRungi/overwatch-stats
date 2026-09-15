import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()
api_url = "https://overfast-api.tekrop.fr"

@router.get("/players/{battle_tag}")
async def get_player_stats(battle_tag: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/players/{battle_tag}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.json()
        )

    return response.json()
