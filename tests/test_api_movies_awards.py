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
@allure.story("Поиск фильма и его наград")
@pytest.mark.api
def test_find_film_and_awards(api):
    film_name = "Джентльмены"

    # ── Шаг 1. Поиск фильма ──
    with allure.step(f"Поиск фильма '{film_name}'"):
        search_result = api.search_movies(query=film_name, limit=5, page=1)

        assert "docs" in search_result, "В ответе нет ключа 'docs'"
        assert len(search_result["docs"]) > 0, "Фильмы не найдены"

        film = search_result["docs"][0]
        film_id = film["id"]
        _attach_json("First Film from Search", film)
        allure.attach(str(film_id), name="Film ID",
                       attachment_type=allure.attachment_type.TEXT)

        # Проверяем релевантность
        name = film.get("name", "")
        alt_name = film.get("alternativeName", "")
        searchable = (name or alt_name).lower()
        assert (film_name.lower() in searchable
                or searchable in film_name.lower()), (
            f"Название '{searchable}' не совпадает с запросом '{film_name}'"
        )

    # ── Шаг 2. Получение полных данных о фильме по ID ──
    with allure.step(f"Получение фильма по ID={film_id}"):
        movie_details = api.get_movie_by_id(film_id)
        assert movie_details.get("id") == film_id, (
            f"ID в ответе {movie_details.get('id')} не совпадает с {film_id}"
        )
        _attach_json("Movie Details", movie_details)

        # Проверка обязательных полей
        assert "name" in movie_details or "alternativeName" in movie_details, (
            "У фильма нет ни name, ни alternativeName"
        )
        assert "type" in movie_details, "У фильма нет поля 'type'"
        assert movie_details["type"], "type не должен быть пустым"

    # ── Шаг 3. Получение наград фильма ──
    with allure.step(f"Получение наград фильма ID={film_id}"):
        awards = api.get_movie_awards(film_id, limit=50)
        _attach_json("Movie Awards", awards)

        # Структура ответа
        assert "docs" in awards, "В ответе наград нет ключа 'docs'"
        awards_list = awards["docs"]
        allure.attach(str(len(awards_list)), name="Awards Count",
                       attachment_type=allure.attachment_type.TEXT)

        if len(awards_list) > 0:
            # Проверяем структуру первой награды
            first_award = awards_list[0]
            assert "movieId" in first_award or "movie" in first_award, (
                "У награды нет ссылки на фильм (movieId/movie)"
            )
            assert "nomination" in first_award, (
                "У награды нет поля 'nomination'"
            )
            # nomination может содержать award.title, year
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
                "Награды не найдены — это допустимо для некоторых фильмов",
                name="No Awards",
                attachment_type=allure.attachment_type.TEXT,
            )
