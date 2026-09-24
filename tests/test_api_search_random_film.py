import os
import requests
import allure
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


@allure.feature("API")
@allure.story("Поиск рандомного фильма")
@pytest.mark.api
def test_find_actress_and_awards():

    with (allure.step(f"Поиск рандомного фильма:")):
        search_url = f"{BASE_URL}/v1.4/movie/random"
        headers = {"X-API-KEY": API_KEY}
        params = {"type": "movie",
                  "notNullFields" : ["name" , "description"],
                  "rating.kp" :"7-10",
                  "year" :"2020 - 2025",
                  }

        resp = requests.get(search_url, headers=headers, params=params)
        assert resp.status_code == 200, f"Search failed: {resp.status_code}"

        docs = resp.json()
        assert len(docs) > 0, "No persons found in search result"

