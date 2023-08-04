from typing import Optional


class SoupNotFoundError(Exception):
    def __init__(self):
        super().__init__('Soup not found.')


class TagNotFoundError(Exception):
    def __init__(self, tag_type: str, attrs: Optional[dict[str, str]] = None):
        message = [f'Tag of type <{tag_type}>, ']
        if attrs is not None:
            message.append('with attributes: ')
            for key, val in attrs.items():
                message.append(f'{key} = {val}, ')
        message.append('not found.')
        super().__init__(''.join(message))


class UrlNotFoundError(Exception):
    def __init__(self, parent_url: str, page_string: str):
        super().__init__(
            f'Url, with parent: {parent_url}, '
            f'and page identifier: {page_string}, not found.'
        )


class CompetitionNotSupportedError(Exception):
    def __init__(self, competition_name: str) -> None:
        super().__init__(
            f'Data for competition: {competition_name} unavailable'
            'as it is not currently supported.'
        )
