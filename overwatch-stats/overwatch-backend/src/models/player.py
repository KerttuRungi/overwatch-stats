from sqlmodel import Field, SQLModel

class Players(SQLModel, table=True):
    __tablename__ = "players"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    avatar: str = Field(nullable=False)
    namecard: str = Field(nullable=False)

