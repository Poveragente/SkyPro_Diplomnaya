import os
import json
import allure
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

if not BASE_URL or not API_KEY:
    pytest.skip("Не заданы BASE_URL или API_KEY", allow_module_level=True)

def _attach_json(name, data):
    allure.attach(
        name=name,
        body=json.dumps(data, ensure_ascii=False, indent=2),
        attachment_type=allure.attachment_type.JSON,
    )

@allure.feature("API")
@allure.story("Поиск актрисы и её наград")
@pytest.mark.api
def test_find_actress_and_awards(api):
    actress_name = "Марго Робби"

    # ── Шаг 1. Поиск персоны ──
    with allure.step(f"Поиск персоны '{actress_name}'"):
        search_result = api.search_persons(query=actress_name, limit=5, page=1)

        assert "docs" in search_result, "В ответе нет ключа 'docs'"
        assert len(search_result["docs"]) > 0, "Персоны не найдены"

        person = search_result["docs"][0]
        person_id = person["id"]
        _attach_json("First Person from Search", person)
        allure.attach(str(person_id), name="Person ID",
                       attachment_type=allure.attachment_type.TEXT)

        # Проверяем релевантность
        name = person.get("name", "")
        en_name = person.get("enName", "")
        searchable = (name or en_name).lower()
        assert (actress_name.lower() in searchable
                or searchable in actress_name.lower()), (
            f"Имя '{searchable}' не совпадает с запросом '{actress_name}'"
        )

    # ── Шаг 2. Проверка профессии ──
    with allure.step("Проверка, что персона является актрисой"):
        # Получаем полные данные
        person_details = api.get_person_by_id(person_id)
        _attach_json("Person Details", person_details)

        professions = person_details.get("profession", [])
        prof_names = [p.get("value", "") if isinstance(p, dict) else str(p)
                      for p in professions]
        allure.attach(str(prof_names), name="Professions",
                       attachment_type=allure.attachment_type.TEXT)

        assert any("актер" in p.lower() or "актрис" in p.lower()
                    for p in prof_names), (
            f"Профессия 'актер/актриса' не найдена среди: {prof_names}"
        )

    # ── Шаг 3. Получение наград персоны ──
    with allure.step(f"Получение наград персоны ID={person_id}"):
        awards = api.get_person_awards(person_id, limit=50)
        _attach_json("Person Awards", awards)

        assert "docs" in awards, "В ответе наград нет ключа 'docs'"
        awards_list = awards["docs"]
        allure.attach(str(len(awards_list)), name="Awards Count",
                       attachment_type=allure.attachment_type.TEXT)

        if len(awards_list) > 0:
            first_award = awards_list[0]
            assert "personId" in first_award or "person" in first_award, (
                "У награды нет ссылки на персону (personId/person)"
            )
            assert "nomination" in first_award, (
                "У награды нет поля 'nomination'"
            )
            nom = first_award["nomination"]
            if isinstance(nom, dict):
                assert "title" in nom or "award" in nom, (
                    "В nomination нет ни 'title', ни 'award'"
                )
            allure.attach(
                json.dumps(first_award, ensure_ascii=False, indent=2),
                name="First Award",
                attachment_type=allure.attachment_type.JSON,
            )
        else:
            allure.attach(
                "Награды не найдены — это допустимо",
                name="No Awards",
                attachment_type=allure.attachment_type.TEXT,
            )

