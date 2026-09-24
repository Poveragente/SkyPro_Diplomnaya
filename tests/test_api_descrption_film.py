import os
import requests
import allure
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


@allure.feature("API")
@allure.story("Поиск описания Фильма по названию")
@pytest.mark.api
def test_find_actress_and_awards():
    film_name = "Сезимдер"

    with allure.step(f"Поиск фильма {film_name}"):
        search_url = f"{BASE_URL}/v1.4/movie/search"
        headers = {"X-API-KEY": API_KEY}
        params = {"query": film_name, "page": 1, "limit": 1}

        resp = requests.get(search_url, headers=headers, params=params)
        assert resp.status_code == 200, f"Search failed: {resp.status_code}"

        docs = resp.json()
        assert len(docs.get("docs", [])) > 0, "No films found in search result"

        film_id = docs["docs"][0]["id"]
        allure.attach(
            name="Found personId",
            body=str(film_id),
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"вывод описания {film_name}"):
        search_url = f"{BASE_URL}/v1.4/movie"
        headers = {"X-API-KEY": API_KEY}
        params = {"id": film_id}

        resp = requests.get(search_url, headers=headers, params=params)
        assert resp.status_code == 200, f"Search failed: {resp.status_code}"

        docs = resp.json()

        assert len(docs) > 0, "Нет данных в docs"


