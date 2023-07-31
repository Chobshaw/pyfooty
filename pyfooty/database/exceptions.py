class CompetitionNotFoundError(Exception):
    def __init__(self, competition_name) -> None:
        super().__init__(f'Competition not found, name: {competition_name}')
