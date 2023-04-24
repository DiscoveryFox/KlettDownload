import keyring
import webdriver_manager.chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Type
import typing

from . import BookProvider, BackendDoesntExistError, BackendAlreadyExistError
from . import Klett


class BookHandler:
    def __init__(self, backends: typing.List[Type[BookProvider]]):
        self.backends_backup = backends
        self.backend = {
            book_backend.backend_name: book_backend for book_backend in backends
        }

    def save_book(
        self,
        identifier: str,
        backend: str | Type[BookProvider],
        scale: int,
        download_dir: str = None,
        page_offset: int = 0,
    ):
        if isinstance(backend, BookProvider):
            if not self.backend[backend.backend_name]:
                self.backend[backend.backend_name] = backend
            backend_str: str = backend.backend_name
        elif type(backend) is not str:
            raise TypeError(
                f"Backend has to be type of Str or subclass of Bookprovider not "
                f"{type(backend)}"
            )
        else:
            backend_str: str = backend
        backend_str: str
        if backend_str not in self.backend.keys():
            raise BackendDoesntExistError(
                f"Backend with the name {backend_str} isn't found in your "
                f"backend config."
            )
        Provider: Type[BookProvider] = self.backend[backend_str]
        Provider.download_book(
            identifier=identifier,
            download_dir=download_dir,
            page_offset=page_offset,
            scale=scale,
        )

    def add_backend(self, backend: Type[BookProvider]):
        if backend.backend_name in self.backend.keys():
            raise BackendAlreadyExistError
        else:
            self.backend[backend.backend_name] = backend
