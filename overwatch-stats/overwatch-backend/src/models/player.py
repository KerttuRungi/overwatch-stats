from sqlmodel import Field, SQLModel

class Players(SQLModel, table=True):
    __tablename__ = "players"

    id: int = Field(default=None, primary_key=True)
    battle_tag: str = Field(index=True, nullable=False)
    name: str = Field(nullable=False)
    is_public: bool = Field(default=True, nullable=False)
