from models.player_stats import PlayerStats

class PlayerStatsRepository:
    def __init__(self, session):
        self.session = session

    def add_many(self, stats: list[PlayerStats]) -> list[PlayerStats]:
        self.session.add_all(stats)
        self.session.commit()

        return stats
