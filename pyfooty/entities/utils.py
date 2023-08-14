from datetime import datetime
from functools import cache


@cache
def get_current_year() -> int:
    return datetime.utcnow().year
