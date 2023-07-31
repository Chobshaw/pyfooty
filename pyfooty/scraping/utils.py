import pandas as pd

from global_utils import constants
from scraping._local_utils import _find_url_from_base


def get_countries() -> list[str]:
    countries_url = _find_url_from_base(
        parent_url=constants.BASE_DATA_URL, page_string='Countries'
    )
    countries_df = pd.read_html(countries_url, attrs={'id': 'countries'})[0]
    return countries_df.Country.map(lambda x: x.lower()).to_list()


def get_valid_countries() -> tuple[str, ...]:
    return constants.VALID_COUNTRIES


def get_valid_competitions() -> tuple[str, ...]:
    return tuple(constants.COMPETITIONS_DICT.keys())
