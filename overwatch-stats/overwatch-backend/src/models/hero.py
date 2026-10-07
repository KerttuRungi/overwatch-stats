from sqlmodel import Field, SQLModel

class Heroes(SQLModel, table=True):
    __tablename__ = "heroes"

    key: str = Field(primary_key=True)
    name: str = Field(nullable=False)
    role: str = Field(nullable=False)
