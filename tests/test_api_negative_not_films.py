import json
import allure
import pytest


@allure.feature("API: Поиск фильмов")
@allure.story("Негативные сценарии поиска")
@pytest.mark.api
def test_search_nonexistent_movie(api):
    """
    Негативный кейс: поиск фильма по несуществующему названию.
    Ожидаем: статус 200 + пустой массив docs.
    """
    query = "ФильмКоторогоНетНик"

    with allure.step(f"Поиск по запросу '{query}'"):
        data = api.search_movies(query=query, limit=10, page=1)

    allure.attach(
        name="Response body",
        body=json.dumps(data, ensure_ascii=False, indent=2),
        attachment_type=allure.attachment_type.JSON,
    )

    with allure.step("Проверяем структуру ответа"):
        assert "docs" in data, "В ответе отсутствует поле 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' не является списком"

    with allure.step("Проверяем, что результатов нет"):
        assert len(data["docs"]) == 0, (
            f"Ожидался пустой список, получено {len(data['docs'])} элементов"
        )

    with allure.step("Проверяем пагинацию"):
        assert data.get("total") == 0, "total должен быть 0 при отсутствии результатов"
        assert data.get("pages") == 0, "pages должен быть 0 при отсутствии результатов"
