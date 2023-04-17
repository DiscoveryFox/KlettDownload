import typing

import requests


class CookieNotFound(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class AuthNotStored(KeyError):
    def __init__(self, *args):
        super().__init__(*args)


class BookProvider:
    _service_name: str = "LubaProject"
    _service_type: str

    @classmethod
    def get_session_cookie(cls, email: str = None, password: str = None) -> str:
        ...

    @classmethod
    def get_auth_credentials(
        cls,
    ) -> typing.Tuple[str, str] | None:
        ...

    @classmethod
    def store_auth_credentials(cls, email: str, password: str) -> None:
        ...

    @classmethod
    def get_max_pages(cls, book_id: str, session_cookie: str) -> int:
        # TODO: Maybe automatically detect page offset in the future.
        ...

    @classmethod
    def get_page(
        cls,
        page_number: int,
        book_id: str,
        page_offset: int,
        scale: typing.Union[1, 2, 4],
        session_cookie: str = None,
    ) -> bytes:
        ...

    @classmethod
    def get_all_book_ids(cls) -> ...:
        ...
