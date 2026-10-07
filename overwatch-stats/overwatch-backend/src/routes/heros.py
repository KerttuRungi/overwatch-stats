import os
import httpx
from models.hero import Heroes
from schemas import HeroSummary
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()

load_dotenv()

api_url = os.getenv("OVERFAST_API_URL")

async def fetch_heroes_from_overfast(client: httpx.AsyncClient) -> list[Heroes]:
    try:
        response = await client.get(f"{api_url}/heroes")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach the stats API.")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return [Heroes(key=hero["key"], name=hero["name"], role=hero["role"]) for hero in response.json()]

@router.get("/heroes")
async def get_heroes() -> list[HeroSummary]:

    async with httpx.AsyncClient(timeout=30) as client:
        heroes = await fetch_heroes_from_overfast(client)

    return [HeroSummary(key=hero.key, name=hero.name, role=hero.role) for hero in heroes]
