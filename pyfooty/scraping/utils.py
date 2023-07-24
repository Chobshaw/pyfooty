import re


def split_on_dash_or_endash(string: str) -> list:
    pattern = r'[-\u2013]'
    return re.split(pattern, string)
