from functools import cache, partial
import re
from typing import Optional

from bs4 import BeautifulSoup
import requests

from global_utils import constants
from scraping._exceptions import (
    SoupNotFoundError,
    TagNotFoundError,
    UrlNotFoundError,
)


def _split_on_dash_or_endash(string: str) -> list:
    pattern = r'[-\u2013]'
    return re.split(pattern, string)


@cache
def _get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def _find_rel_url(soup: BeautifulSoup, page_string: str | re.Pattern) -> str:
    if soup is None:
        raise SoupNotFoundError
    anchor_tag = soup.find('a', string=page_string)
    if anchor_tag is None:
        raise TagNotFoundError('a', attrs={'string': page_string})
    return anchor_tag.get('href')


@cache
def _find_url(
    parent_url: str,
    page_string: str | re.Pattern,
    table_id: Optional[str] = None,
    *,
    base_url: Optional[str] = None,
) -> str:
    base_url = parent_url if not base_url else base_url
    soup = _get_soup(parent_url)

    try:
        if table_id is not None:
            table = soup.find('table', id=table_id)
            rel_url = _find_rel_url(table, page_string)
        else:
            rel_url = _find_rel_url(soup, page_string)
    except (SoupNotFoundError, TagNotFoundError):
        response = requests.get(parent_url)
        response.raise_for_status()
        raise UrlNotFoundError(parent_url, page_string)
    return base_url + rel_url


_find_url_from_base = partial(_find_url, base_url=constants.BASE_DATA_URL)
