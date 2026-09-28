import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from config import HEADLESS, TIMEOUT, BASE_URL
from pages.api_class_page import ApiPage
import os
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        raise ValueError("BASE_URL не задан в .env")
    return url


@pytest.fixture
def api_key():
    key = os.getenv("API_KEY")
    if not key:
        pytest.skip("Не задан API_KEY")
    return key

@pytest.fixture
def api_headers(api_key):
    return {"X-API-KEY": api_key}

@pytest.fixture
def api(api_headers):
    return ApiPage(BASE_URL, api_headers, api_version="v1.5")

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
