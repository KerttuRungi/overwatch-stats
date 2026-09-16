from sqlmodel import select
from src.models.player import Players


class PlayersRepository:
    def __init__(self, session):
        self.session = session

    def get_player_by_user(self, username: str) -> Players | None:
        statement = select(Players).where(Players.username == username)
        return self.session.execute(statement).scalars().first()

    def add (self, player: Players) -> Players:
        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)
        return player