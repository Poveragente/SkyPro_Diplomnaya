import os
import json
import requests
import allure
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


@allure.feature("API")
@allure.story("Поиск актрисы и её наград")
@pytest.mark.api
def test_find_actress_and_awards():
    actress_name = "Николь Кидман"

    with allure.step(f"Поиск актрисы: {actress_name}"):
        search_url = f"{BASE_URL}/v1.5/person/search"
        headers = {"X-API-KEY": API_KEY}
        params = {"query": actress_name, "page": 1, "limit": 1}

        resp = requests.get(search_url, headers=headers, params=params)
        assert resp.status_code == 200, f"Search failed: {resp.status_code}"

        docs = resp.json()
        assert len(docs.get("docs", [])) > 0, "No persons found in search result"

        person_id = docs["docs"][0]["id"]
        allure.attach(
            name="Found personId",
            body=str(person_id),
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Получение наград для personId={person_id}"):
        awards_url = f"{BASE_URL}/v1.5/person/awards"
        params_awards = {
            "personId": person_id,
            "limit": 10,
            "sortField": "nomination.award.year",
            "sortType": "-1",
            "selectFields": ["personId", "winning", "nomination"],
        }

        resp_awards = requests.get(awards_url, headers=headers, params=params_awards)
        assert (
            resp_awards.status_code == 200
        ), f"Awards request failed: {resp_awards.status_code}"
        awards_data = resp_awards.json()

        allure.attach(
            name="Awards response",
            body=json.dumps(awards_data, ensure_ascii=False, indent=2),
            attachment_type=allure.attachment_type.JSON,
        )

    awards_docs = awards_data.get("docs", [])

    # 1. Список не пустой
    assert len(awards_docs) > 0, "Награды не найдены"

    # 2. Каждая награда имеет nomination
    for award in awards_docs:
        assert "nomination" in award, f"Награда не содержит nomination: {award}"

    # 3. Номинация содержит премию с названием и годом
    for award in awards_docs:
        nom = award["nomination"]
        assert "award" in nom, f"Номинация не содержит award: {nom}"
        award_info = nom["award"]
        assert "title" in award_info, f"Премия не содержит title: {award_info}"
        assert "year" in award_info, f"Премия не содержит year: {award_info}"

    # 4. Если API вернул personId — проверяем, что он совпадает
    for award in awards_docs:
        if "personId" in award:
            assert (
                award["personId"] == person_id
            ), f"personId в награде ({award['personId']}) не совпадает с ожидаемым ({person_id})"

    # 5. Если API вернул winning — проверяем, что это boolean
    for award in awards_docs:
        if "winning" in award:
            assert isinstance(
                award["winning"], bool
            ), f"winning должен быть boolean: {award['winning']}"
