import typing
import requests


class CookieNotFoundError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class AuthNotStoredError(KeyError):
    def __init__(self, *args):
        super().__init__(*args)


class BookNotOwnedError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class PageNotFoundError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class BackendDoesntExistError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class BackendAlreadyExistError(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class BookProvider:
    _service_name: str = "LubaProject"
    _service_type: str
    backend_name: str

    @classmethod
    def get_session_cookie(cls, email: str = None, password: str = None) -> str:
        pass

    @classmethod
    def get_auth_credentials(
        cls,
    ) -> typing.Tuple[str, str] | None:
        pass

    @classmethod
    def store_auth_credentials(cls, email: str, password: str) -> None:
        pass

    @classmethod
    def get_max_pages(cls, book_id: str, session_cookie: str = None) -> int:
        # TODO: Maybe automatically detect page offset in the future.
        pass

    @classmethod
    def get_page_content(
        cls,
        page_number: int,
        book_id: str,
        page_offset: int,
        scale: typing.Union[1, 2, 4],
        session_cookie: str = None,
    ) -> bytes:
        pass

    @classmethod
    def get_all_book_ids(cls, link: bool = False) -> typing.List[str]:
        pass

    @classmethod
    def download_page(
        cls,
        page_number: int,
        book_id: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> None:
        pass

    @classmethod
    def download_book(
        cls,
        identifier: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> None:
        pass
