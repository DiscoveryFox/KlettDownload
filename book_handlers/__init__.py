import keyring
import webdriver_manager.chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Type

from models import BookProvider
from klett import Klett


class BookHandler:
    def __init__(self):
        ...

    def save_book(self, book_id: str, book_provider_class: Type[BookProvider]):
        print(book_provider_class.get_max_pages(book_id))
        print(book_provider_class.get_all_book_ids())


if __name__ == "__main__":
    handler = BookHandler()
    handler.save_book("PPL-DQUXYZ6VPH", Klett)
