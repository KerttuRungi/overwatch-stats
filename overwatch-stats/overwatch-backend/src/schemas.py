from pydantic import BaseModel

class PlayerProfileEndorsementResponse(BaseModel):
    level: int
    
class PlayerProfileSummary(BaseModel):
    username: str
    avatar: str
    namecard: str
    #endorsement: PlayerProfileEndorsementResponse

class HeroSummary(BaseModel):
    key: str
    name: str
    role: str

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

class RoleStats(BaseModel):
    games_played: int
    games_won: int
    time_played: int
    winrate: float

class PlayerStatsData(BaseModel):
    general: GeneralStats | None = None
    heroes: list[HeroStats] = []
    roles: dict[str, RoleStats] = {}

class PlayerStatsComparison(BaseModel):
    username: str
    avatar: str
    general: GeneralStats | None = None
    top_heroes: list[HeroStats] = []
    error: str | None = None

class StatsComparisonResponse(BaseModel):
    players: list[PlayerStatsComparison]
    most_wins: list[str]

class PlayerRoleProfile(BaseModel):
    username: str
    avatar: str
    main_role: str | None = None
    role_hours: dict[str, float] = {}
    top_heroes: list[HeroStats] = []
    error: str | None = None

class RoleAssignment(BaseModel):
    username: str
    assigned_role: str
    main_role: str
    fit: float

class RoleSuggestion(BaseModel):
    username: str
    from_role: str
    to_role: str
    fit: float
    message: str

class TeamCompatibilityResponse(BaseModel):
    players: list[PlayerRoleProfile]
    assignments: list[RoleAssignment]
    open_slots: list[str]
    substitutes: list[str]
    score: int
    compatible: bool
    warnings: list[str]
    suggestions: list[RoleSuggestion]