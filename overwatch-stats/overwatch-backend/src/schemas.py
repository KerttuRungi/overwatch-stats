from pydantic import BaseModel

class PlayerProfileEndorsementResponse(BaseModel):
    level: int
    
class PlayerProfileSummary(BaseModel):
    username: str
    avatar: str
    namecard: str
    endorsement: PlayerProfileEndorsementResponse