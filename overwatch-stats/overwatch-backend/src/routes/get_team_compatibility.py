import httpx
from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.heroes_repository import HeroesRepository
from repositories.players_list_repository import PlayersRepository
from routes.get_player_stats import get_all_player_results
from schemas import PlayerStatsData, TeamCompatibilityResponse
from services.heroes_service import HeroesService
from services.player_roles_service import build_role_profile
from services.team_compatibility_service import check_compatibility

router = APIRouter()


@router.get("/players/comparison-list/team-compatibility")
async def get_team_compatibility(session: Session = Depends(get_session)) -> TeamCompatibilityResponse:
    players = PlayersRepository(session).get_all_players()
    heroes_service = HeroesService(HeroesRepository(session))

    async with httpx.AsyncClient(timeout=30) as client:
        results = await get_all_player_results(client, players, general=False, heroes=True)

        played = {hero.hero for result in results if isinstance(result, PlayerStatsData) for hero in result.heroes}
        role_map = await heroes_service.get_role_map(client, played)

    profiles = [build_role_profile(player, result, role_map) for player, result in zip(players, results)]
    return check_compatibility(profiles)
