import json
from pathlib import Path
from database.enums import CompetitionFormat, CompetitionType, Gender, TeamType
from database.schemas import Competition


def get_competition_dict() -> dict[str, Competition]:
    pyfooty_path = Path(__file__).parent.parent
    competitions_file_path = pyfooty_path / 'global_utils/competitions.json'
    with open(competitions_file_path, 'r') as file:
        competitions_dict = json.load(file)
    for competition_name, data in competitions_dict.items():
        competitions_dict[competition_name] = Competition(
            name=data['name'],
            gender=Gender.from_value(data['gender']),
            country=data['country'],
            tier=data['tier'],
            competition_type=CompetitionType.from_value(
                data['competition_type']
            ),
            competition_format=CompetitionFormat.from_value(
                data['competition_format']
            ),
            team_type=TeamType.from_value(data['team_type']),
            alt_name=data['alt_name'],
        )
    return competitions_dict
