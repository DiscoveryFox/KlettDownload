import os
import webdriver_manager.chrome
import time
import requests
import selenium
import selenium.webdriver
import tqdm
from seleniumwire import webdriver
import selenium.webdriver.support
import selenium.webdriver.support.ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait  #
from selenium.webdriver.common.keys import Keys
import sys
import getpass
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.disabled = True

load_dotenv()

already_printed_folder = False

USEREMAIL = os.getenv("USEREMAIL")
PASSWORD = os.getenv("PASSWORD")


if USEREMAIL is None:
    USEREMAIL = input("Please provide your Email Adress: ")
if PASSWORD is None:
    PASSWORD = getpass.getpass(
        "Please enter the Password for your Email Address and don't be "
        "confused if you won't see your input, it's hidden: "
    )

logging.basicConfig(level=logging.CRITICAL)  # Main app runs at DEBUG level
logger = logging.getLogger("seleniumwire")
logger.disabled = True
# logger.setLevel(logging.CRITICAL)  # Run selenium wire at ERROR level


def _get_max_pages(id: str, auth_cookie: str, driver):
    """Old try propably failed cus maybe the redirect is triggered by javascript
    req = requests.get(f'https://bridge.klett.de/{id}/?page=max',
                       headers={
                           "cookie": auth_cookie
                       }
                    )

    for resp in req.history:
        print('History')
        print(resp.status_code, resp.url)
    print('No History')
    final_url = req.url.split('page=')[1]
    print(final_url)
    return int(final_url)
    """
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    previous_number = 0
    for number in range(0, 1000):
        # TODO: Maybe decrease this number a little bit since it wastes a lot of performance. We
        #  just need the biggest ebook from klett

        driver.get(f"https://bridge.klett.de/{id}/?page={number}")
        actual_number = int(driver.current_url.split("page=")[1])

        if actual_number == previous_number:
            break
        else:
            previous_number = number

    max_pages = int(driver.current_url.split("page=")[1])
    # driver.execute_script('window.close();')
    driver.switch_to.window(driver.window_handles[0])
    return max_pages


def get_max_pages(book_id: str, session_cookie: str = None, *args, **kwargs) -> int:
    # if not session_cookie:
    # session_cookie = Klett.get_session_cookie()
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


def get_page_klett(
    page_number: int, book_id: str, session_cookie: str, page_offset: int
):
    """
    curl 'https://bridge.klett.de/PPL-X2BDKHZCTB/content/pages/page_173/Scale1.png' \
        -H 'authority: bridge.klett.de' \
        -H 'accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
        -H 'accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7' \
        -H 'cache-control: no-cache' \
        -H 'cookie: klett_session=9c8758a62b36d22df541a35c77e0e8c2; SERVERID=backend1; SESSION=MjBmNWNjMzktMDA4MS00M2UwLWI3ZGQtY2Y0ZGIyYTIzYjRh' \
        -H 'pragma: no-cache' \
        -H 'referer: https://bridge.klett.de/PPL-X2BDKHZCTB/?page=174' \
        -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
        -H 'sec-ch-ua-mobile: ?1' \
        -H 'sec-ch-ua-platform: "Android"' \
        -H 'sec-fetch-dest: image' \
        -H 'sec-fetch-mode: no-cors' \
        -H 'sec-fetch-site: same-origin' \
        -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36' \
    --compressed

    """
    with open(f"{book_id}/page_{page_number + page_offset}.png", "wb") as picture:
        picture.write(
            requests.get(
                # f'https://bridge.klett.de/{book_id}/?page={page_number}',
                f"https://bridge.klett.de/{book_id}/content/pages/page_{page_number}/Scale2.png",
                headers={"cookie": session_cookie},
            ).content
        )
    return already_printed_folder


# TODO: Change the driver back to normal and then request the book with the driver who catches
#  the requests. U need to enter password then in a custom gui.

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--headless")
options.add_argument("--disable-logging")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(
    webdriver_manager.chrome.ChromeDriverManager().install(), chrome_options=options
)

driver.get("https://schueler.klett.de/arbeitsplatz")

WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "username")))

username_field = driver.find_element(By.ID, "username")

password_field = driver.find_element(By.ID, "password")

login_button = driver.find_element(By.ID, "kc-login")

username_field.send_keys(USEREMAIL)
password_field.send_keys(PASSWORD)
login_button.click()

WebDriverWait(driver, 100).until_not(EC.title_contains("Login"))

WebDriverWait(driver, 100).until(EC.title_contains("eBook"))

# print(len(driver.find_elements(By.TAG_NAME,
#                               'img')))

WebDriverWait(driver, 100).until(
    lambda web_driver_wait_driver: len(
        web_driver_wait_driver.find_elements(By.TAG_NAME, "img")
    )
    > 3
)

book_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "https://bridge.klett.de/")

book_links2 = driver.find_elements(By.CSS_SELECTOR, "[rel=noopener]")
book_links2 = [link for link in book_links2 if link.text.replace(" ", "") != "Hilfe"]

# print(book_links2)
book_links3: list = []
for link in book_links2:
    book_links3.append({"text": link.text, "url": link.get_attribute("href")})


def get_cookie(driver):
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])
    url = book_links3[0]["url"]
    print(url)
    print(type(url))
    driver.get(url)
    page_loading = [load for load in driver.requests if load.url == url][1]

    header = page_loading.headers
    for entry in header:
        try:
            if entry == "cookie":
                session_cookie = header["cookie"]
                driver.switch_to.window(driver.window_handles[0])
                return session_cookie

        except IndexError:
            # print('IndexError in get_cookie() function')
            sys.exit(-1)


session_cookie = get_cookie(driver)
print(session_cookie)

for link in book_links3:
    # print(link)
    text = link["text"]
    url = link["url"]
    # print(url)
    book_id = url.replace("https://bridge.klett.de/", "").replace("/", "")
    # print()
    # driver.execute_script('window.open()')
    # driver.switch_to.window(driver.window_handles[1])
    # driver.get(url)

    # page_loading = [load for load in driver.requests if load.url ==
    #                url][1]

    # header = page_loading.headers
    # for entry in header:
    #    try:
    #        if entry == 'cookie':
    #            session_cookie = header['cookie']
    """
                max_pages = driver.find_element(By.XPATH,
                                                '/html/body/div/footer/div[2]/nav[2]/div[1]/div['
                                                '1]/span')
                max_pages.click()
                new_max_pages = driver.find_element(By.XPATH,
                                                    '/html/body/div/footer/div[2]/nav[2]/div[1]/div[1]/form/input')
                new_max_pages.send_keys(Keys.ARROW_LEFT)
                new_max_pages.send_keys(Keys.DELETE)
                new_max_pages.send_keys('V')
                new_max_pages.send_keys(Keys.ENTER)
                time.sleep(1)
                driver.find_element(By.XPATH,
                                    '/html/body/div/footer/div[2]/nav[2]/div[1]/button[2]').click()
                max_pages = driver.find_element(By.XPATH,
                                                '/html/body/div/footer/div[2]/nav[2]/div[1]/div[1]/span')
                max_pages_number = max_pages.text.split('/')[0]
                print(max_pages_number)
                """
    # driver.switch_to.window(driver.window_handles[0])

    max_pages_number = get_max_pages(
        book_id=book_id, session_cookie=session_cookie, driver=driver
    )
    # print(f'Max pages for {book_id}: \n{max_pages_number}')
    already_printed_folder = False
    try:
        os.mkdir(os.getcwd() + "/" + book_id)
    except OSError:
        # print(f'Folder {book_id} already exists. Just updating the pictures.')
        pbar = tqdm.tqdm(total=max_pages_number + 2, desc=f"{book_id}")

        for page in range(max_pages_number + 2):
            get_page_klett(
                page_number=page,
                book_id=book_id,
                session_cookie=session_cookie,
                page_offset=-3,
            )
            pbar.update()
    # except IndexError:
    #    print('IndexError')
    #    sys.exit(-1)
