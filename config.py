import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.kinopoisk.ru")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.kinopoisk.example.com")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
