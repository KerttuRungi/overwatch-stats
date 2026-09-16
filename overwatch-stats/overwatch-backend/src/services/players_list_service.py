from src.models.player import Players
from pydantic import BaseModel

class PlayersListCreate(BaseModel):
    username: str
    avatar: str
    namecard: str
    endorsement_level: int

class PlayersService:
    def add_comparison_player(self, player_data: PlayersListCreate):
        existing_player = self.repository.get_by_user(player_data.username)
        if existing_player:
            raise ValueError(f"Player with username {player_data.username} already exists.")
        add_player = Players(
            username=player_data.username,
            avatar=player_data.avatar,
            namecard=player_data.namecard,
            endorsement_level=player_data.endorsement_level
        )
        return self.repsository.add(add_player)