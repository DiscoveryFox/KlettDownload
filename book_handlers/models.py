import typing
import customtkinter as ctk
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
    ) -> typing.Generator:
        pass

    @classmethod
    def _download_book(
        cls,
        identifier: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> typing.Generator:
        pass

    @classmethod
    def ask_for_auth_ui(cls) -> typing.Tuple[ctk.CTk, ctk.StringVar, ctk.StringVar]:
        ask_for_credentials_window = ctk.CTk()
        # ask_for_credentials_window.resizable(False, False)
        credentials_frame: ctk.CTkFrame = ctk.CTkFrame(ask_for_credentials_window)
        credentials_frame.pack(pady=10, padx=10)

        email_label: ctk.CTkLabel = ctk.CTkLabel(credentials_frame, text="Email")

        email: ctk.StringVar = ctk.StringVar(ask_for_credentials_window)
        email_entry: ctk.CTkEntry = ctk.CTkEntry(
            credentials_frame, textvariable=email, width=200
        )

        password_label: ctk.CTkLabel = ctk.CTkLabel(credentials_frame, text="Password")

        password: ctk.StringVar = ctk.StringVar(ask_for_credentials_window)
        password_entry: ctk.CTkEntry = ctk.CTkEntry(
            credentials_frame, textvariable=password, show="*", width=200
        )

        def ok_button_command():
            ask_for_credentials_window.quit()
            ask_for_credentials_window.destroy()

        ok_button: ctk.CTkButton = ctk.CTkButton(
            ask_for_credentials_window, text="Ok", command=ok_button_command
        )

        email_label.grid(row=1, column=1, padx=5, pady=5)
        email_entry.grid(row=1, column=2)
        password_label.grid(row=2, column=1, padx=5, pady=5)
        password_entry.grid(row=2, column=2)
        ok_button.pack(side=ctk.BOTTOM, pady=5)
        return ask_for_credentials_window, email, password

    @classmethod
    def extract_identifier(cls, message) -> str:
        return message
