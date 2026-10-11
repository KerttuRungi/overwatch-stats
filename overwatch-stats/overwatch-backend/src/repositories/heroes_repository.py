from sqlmodel import Session, select

from models.hero import Heroes


class HeroesRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Heroes]:
        return list(self.session.exec(select(Heroes)).all())

    def upsert_many(self, heroes: list[Heroes]) -> None:
        for hero in heroes:
            self.session.merge(hero)
        self.session.commit()
