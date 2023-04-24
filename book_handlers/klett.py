from webdriver_manager.chrome import ChromeDriverManager
import customtkinter as ctk
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import typing
from .models import AuthNotStoredError, BookProvider, BookNotOwnedError
import keyring
import re
import os.path


class Klett(BookProvider):
    _service_type: str = "klett"
    backend_name: str = "Klett"

    @classmethod
    def get_auth_credentials(
        cls,
    ) -> typing.Tuple[str, str] | None:
        credentials = keyring.get_password(cls._service_name, cls._service_type)
        return credentials.split(":") if credentials is not None else None

    @classmethod
    def store_auth_credentials(cls, email: str, password: str) -> None:
        credentials = f"{email}:{password}"
        keyring.set_password(cls._service_name, cls._service_type, credentials)

    @classmethod
    def get_session_cookie(cls, email: str = None, password: str = None) -> str:
        if not email or not password:
            credentials = cls.get_auth_credentials()
            if credentials is None:
                raise AuthNotStoredError(
                    "Password or Email not stored for Klett in System Keyring."
                )
            else:
                email, password = credentials

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--disable-logging")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            chrome_options=options,
        )

        driver.get("https://schueler.klett.de/arbeitsplatz")

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        login_button = driver.find_element(By.ID, "kc-login")

        username_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 100).until_not(EC.title_contains("Login"))

        WebDriverWait(driver, 100).until(EC.title_contains("eBook"))

        WebDriverWait(driver, 100).until(
            lambda web_driver_wait_driver: len(
                web_driver_wait_driver.find_elements(By.TAG_NAME, "img")
            )
            > 3
        )

        all_book_link = [
            link.get_attribute("href")
            for link in driver.find_elements(By.CSS_SELECTOR, "[rel=noopener]")
            if link.text.replace(" ", "") != "Hilfe"
        ]

        driver.get(all_book_link[0])

        page_loading = [
            load for load in driver.requests if load.url == all_book_link[0]
        ][1]

        try:
            return page_loading.headers["cookie"]
        except IndexError:
            raise CookieNotFound("No cookie found in the request.")

    @classmethod
    def get_page_content(
        cls,
        page_number: int,
        book_id: str,
        page_offset: int,
        scale: typing.Union[1, 2, 4],
        session_cookie: str = None,
    ) -> bytes:
        if session_cookie is None:
            session_cookie = cls.get_session_cookie()

        return requests.get(
            f"https://bridge.klett.de/{book_id}/content/pages/page_{page_number + page_offset}/Scal"
            f"e{str(scale)}.png",
            headers={"cookie": session_cookie},
        ).content

    @classmethod
    def get_max_pages(cls, book_id: str, session_cookie: str = None) -> int:
        if not session_cookie:
            session_cookie = cls.get_session_cookie()
        min_page = 1
        max_page = 10000  # maximum possible number of pages
        while True:
            mid_page = (min_page + max_page) // 2
            url = f"https://bridge.klett.de/{book_id}/content/pages/page_{mid_page}/Scale1.png"
            response = requests.head(url, headers={"cookie": session_cookie})
            if response.status_code == 404:
                max_page = mid_page - 1
            else:
                if mid_page == max_page:
                    return mid_page
                min_page = mid_page + 1

    @classmethod
    def get_all_book_ids(cls, link: bool = False) -> typing.List[str]:
        credentials = cls.get_auth_credentials()
        if credentials is None:
            raise AuthNotStoredError(
                "Password or Email not stored for Klett in System Keyring."
            )
        else:
            email, password = credentials

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--disable-logging")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            chrome_options=options,
        )

        driver.get("https://schueler.klett.de/arbeitsplatz")

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")

        login_button = driver.find_element(By.ID, "kc-login")

        username_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 100).until_not(EC.title_contains("Login"))

        WebDriverWait(driver, 100).until(EC.title_contains("eBook"))

        WebDriverWait(driver, 100).until(
            lambda web_driver_wait_driver: len(
                web_driver_wait_driver.find_elements(By.TAG_NAME, "img")
            )
            > 3
        )

        all_book_link = [
            link.get_attribute("href")
            for link in driver.find_elements(By.CSS_SELECTOR, "[rel=noopener]")
            if link.text.replace(" ", "") != "Hilfe"
        ]
        if link:
            return all_book_link
        return [link.split("/")[-1] for link in all_book_link]

    @classmethod
    def download_page(
        cls,
        page_number: int,
        book_id: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> None:
        if book_id not in cls.get_all_book_ids():
            raise BookNotOwnedError(
                f'Book with the ID: "{book_id}" not found in your owned books.'
            )
        if page_number > cls.get_max_pages(book_id=book_id):
            raise PageNotFound(f"Page {page_number} not found in Book {book_id}")
        if not download_dir:
            download_dir: str = book_id
        page_content: bytes = cls.get_page_content(
            page_number=page_number,
            book_id=book_id,
            page_offset=page_offset,
            scale=scale,
        )
        if not os.path.isdir(download_dir):
            os.mkdir(download_dir)

        with open(
            f"{download_dir}/page_{page_number + page_offset}_scale_{str(scale)}.png",
            "wb",
        ) as page:
            page.write(page_content)

    @classmethod
    def _download_book(
        cls,
        identifier: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> None:
        if not download_dir:
            download_dir = identifier
        if identifier not in cls.get_all_book_ids():
            raise BookNotOwnedError(
                f'Book with the ID: "{identifier}" not found in your owned books.'
            )
        for page in range(cls.get_max_pages(book_id=identifier)):
            cls.download_page(
                page_number=page,
                book_id=identifier,
                download_dir=download_dir,
                page_offset=page_offset,
                scale=scale,
            )
    @classmethod
    def download_book(
        cls,
        identifier: str,
        download_dir: str = None,
        page_offset: int = 0,
        scale: int = 4,
    ) -> None:
        if not download_dir:
            download_dir = identifier
        if identifier not in cls.get_all_book_ids():
            raise BookNotOwnedError(
                f'Book with the ID: "{identifier}" not found in your owned books.'
            )
        for page in range(cls.get_max_pages(book_id=identifier)):
            cls.download_page(
                page_number=page,
                book_id=identifier,
                download_dir=download_dir,
                page_offset=page_offset,
                scale=scale,
            )
            yield page
