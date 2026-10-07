import httpx
from dotenv import load_dotenv
from routes.heros import fetch_heroes_from_overfast
from repositories.heroes_repository import HeroesRepository

load_dotenv()

class HeroesService:

    def __init__(self, repository: HeroesRepository):
        self.repository = repository

    async def get_role_map(self, client: httpx.AsyncClient, played: set[str]) -> dict[str, str]:
        role_map = {hero.key: hero.role for hero in self.repository.get_all()}

        if not role_map or not played.issubset(role_map):
            self.repository.upsert_many(await fetch_heroes_from_overfast(client))
            role_map = {hero.key: hero.role for hero in self.repository.get_all()}

        return role_map
