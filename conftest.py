import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from config import HEADLESS, TIMEOUT
from pages.search_page import MovieSearchPage
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        raise ValueError("BASE_URL не задан в .env")
    return url


@pytest.fixture(scope="session")
def api_key():
    key = os.getenv("API_KEY")
    if not key:
        raise ValueError("API_KEY не задан в .env")
    return key


@pytest.fixture
def movie_search_page(base_url, api_key):
    headers = {"X-API-KEY": api_key}
    return MovieSearchPage(base_url=base_url, headers=headers)


@pytest.fixture(scope="session")
def driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(TIMEOUT)
    yield driver
    driver.quit()


@pytest.fixture
def session(driver):
    """Фикстура, которую можно использовать в тестах для доступа к driver."""
    return driver


@pytest.fixture
def movie_search_page(base_url, api_key):
    headers = {"X-API-KEY": api_key}
    return MovieSearchPage(base_url=base_url, headers=headers)
