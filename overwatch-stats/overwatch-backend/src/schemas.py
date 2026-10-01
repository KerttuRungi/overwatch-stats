from pydantic import BaseModel

class PlayerProfileEndorsementResponse(BaseModel):
    level: int
    
class PlayerProfileSummary(BaseModel):
    username: str
    avatar: str
    namecard: str
    #endorsement: PlayerProfileEndorsementResponse

class GeneralStats(BaseModel):
    games_played: int
    games_won: int
    games_lost: int
    time_played: int
    winrate: float

class HeroStats(BaseModel):
    hero: str
    games_played: int
    games_won: int
    time_played: int
    winrate: float

class PlayerStatsComparison(BaseModel):
    username: str
    avatar: str
    general: GeneralStats | None = None
    top_heroes: list[HeroStats] = []
    error: str | None = None

class StatsComparisonResponse(BaseModel):
    players: list[PlayerStatsComparison]
    most_wins: list[str]