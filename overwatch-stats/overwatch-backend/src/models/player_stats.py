from datetime import datetime, timezone
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel

class PlayerStats(SQLModel, table=True):
    __tablename__ = "player_stats"

    id: int = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="players.id", ondelete="CASCADE", index=True, nullable=False)
    games_played: int = Field(nullable=False)
    games_won: int = Field(nullable=False)
    games_lost: int = Field(nullable=False)
    time_played: int = Field(nullable=False)
    winrate: float = Field(nullable=False)
    top_heroes: list[dict] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
