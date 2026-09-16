from pydantic import BaseModel
import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()

class ComparisonPlayerListCreate(BaseModel):
    username: str
    avatar: str
    namecard: str
    endorsement_level: int

@router.post("/comparison-list-players")
async def add_comparison_players(player_data: )

return service.add_comparison_players(player_data)