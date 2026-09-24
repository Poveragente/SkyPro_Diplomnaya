import allure
import pytest


@allure.feature("API: Поиск фильмов")
@allure.story("Негативные сценарии поиска")
@pytest.mark.api
def test_search_nonexistent_movie(movie_search_page):
    """
    Негативный кейс: поиск фильма по несуществующему названию.
    Ожидаем: статус 200 + пустой массив docs.
    """
    query = "ФильмКоторогоНетНик"
    limit = 10
    page = 1

    with allure.step(
        f"Выполняем поиск по запросу '{query}' (limit={limit}, page={page})"
    ):
        response = movie_search_page.search(query=query, limit=limit, page=page)

    allure.attach(
        name="Response status",
        body=str(response.status_code),
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        name="Response body",
        body=response.text,
        attachment_type=allure.attachment_type.JSON,
    )

    # Проверки
    assert (
        response.status_code == 200
    ), f"Ожидался статус 200, получен {response.status_code}"

    data = response.json()

    with allure.step("Проверяем структуру ответа"):
        # В API Кинопоиска список результатов лежит в поле docs, а не results
        assert "docs" in data, "В ответе отсутствует поле 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' не является списком"

    with allure.step("Проверяем, что результатов нет (пустой список)"):
        assert (
            len(data["docs"]) == 0
        ), f"Ожидался пустой список, получено {len(data['docs'])} элементов"

    with allure.step("Опционально: проверяем пагинацию"):
        assert data.get("total") == 0, "total должен быть 0 при отсутствии результатов"
        assert data.get("pages") == 0, "pages должен быть 0 при отсутствии результатов"
