from models.player import Players
from repositories.players_list_repository import PlayersRepository
from schemas import PlayerProfileSummary

class PlayersService:

    def __init__(self, repository: PlayersRepository):
        self.repository = repository
    
    def add_comparison_player(self, player_data: PlayerProfileSummary):
        existing_player = self.repository.get_player_by_user(player_data.username)
        if existing_player:
            raise ValueError(f"Player with username {player_data.username} already exists.")
        
        add_player = Players(
            username=player_data.username,
            avatar=player_data.avatar,
            namecard=player_data.namecard,
        )
        return self.repository.add(add_player)

    def get_all_players(self) -> list[PlayerProfileSummary]:
        players = self.repository.get_all_players()
        return [PlayerProfileSummary(
            username=player.username,
            avatar=player.avatar,
            namecard=player.namecard
        ) for player in players
        ]
    