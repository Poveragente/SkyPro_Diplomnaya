import os
import time
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
@allure.story("Поиск описания фильма по названию")
@pytest.mark.api
def test_find_film_description_by_title(api):
    film_name = "Сезимдер"

    # ── Шаг 1. Поиск фильма ──
    with allure.step(f"Поиск фильма '{film_name}'"):
        search_result = api.search_movies(query=film_name, limit=1, page=1)

        assert "docs" in search_result, "В ответе нет ключа 'docs'"
        assert len(search_result["docs"]) > 0, "Фильмы не найдены"

        # ── Структура верхнего уровня ──
        assert "total" in search_result, "Нет ключа 'total'"
        assert "limit" in search_result, "Нет ключа 'limit'"
        assert "page" in search_result, "Нет ключа 'page'"
        assert "pages" in search_result, "Нет ключа 'pages'"

        assert isinstance(search_result["docs"], list), "'docs' должен быть списком"
        assert isinstance(search_result["total"], int), "'total' должен быть int"
        assert search_result["total"] >= 0, "'total' должен быть >= 0"
        assert search_result["limit"] == 1, f"limit={search_result['limit']}, ожидался 1"

        film = search_result["docs"][0]
        film_id = film["id"]
        _attach_json("First Film from Search", film)

        # Проверка релевантности
        name = film.get("name", "")
        alt_name = film.get("alternativeName", "")
        assert name or alt_name, "Оба поля имени пустые"
        searchable = (name or alt_name).lower()
        assert (film_name.lower() in searchable
                or searchable in film_name.lower()), (
            f"Название '{searchable}' не совпадает с запросом '{film_name}'"
        )

    # ── Шаг 2. Получение описания по ID ──
    with allure.step(f"Получение описания фильма по ID={film_id}"):
        movie_details = api.get_movie_by_id(film_id)
        _attach_json("Movie Details", movie_details)

        assert movie_details.get("id") == film_id, (
            f"ID в ответе {movie_details.get('id')} не совпадает с {film_id}"
        )

        # Проверка описания
        description = movie_details.get("description", "")
        short_description = movie_details.get("shortDescription", "")

        allure.attach(description or "null", name="Description",
                       attachment_type=allure.attachment_type.TEXT)
        allure.attach(short_description or "null", name="Short Description",
                       attachment_type=allure.attachment_type.TEXT)

        assert description or short_description, (
            f"У фильма '{film_name}' (ID={film_id}) нет ни description, "
            "ни shortDescription"
        )

        # Описание не должно быть слишком коротким (псевдо-проверка)
        if description:
            assert len(description) > 10, (
                f"Описание слишком короткое ({len(description)} символов): "
                f"{description[:50]}..."
            )

    # ── Шаг 3. Проверка дополнительных полей ──
    with allure.step("Проверка дополнительных полей фильма"):
        # Год
        year = movie_details.get("year")
        if year is not None:
            assert isinstance(year, int), f"year должен быть int, получен {type(year)}"
            assert year > 1900, f"year={year} слишком маленький"
            allure.attach(str(year), name="Year",
                           attachment_type=allure.attachment_type.TEXT)

        # Рейтинг
        rating = movie_details.get("rating", {})
        if isinstance(rating, dict):
            kp_rating = rating.get("kp")
            if kp_rating is not None:
                assert isinstance(kp_rating, (int, float)), (
                    f"rating.kp должен быть числом, получен {type(kp_rating)}"
                )
                assert 0 <= kp_rating <= 10, (
                    f"rating.kp={kp_rating} вне диапазона 0-10"
                )
                allure.attach(str(kp_rating), name="KP Rating",
                               attachment_type=allure.attachment_type.TEXT)

        # Жанры
        genres = movie_details.get("genres", [])
        if genres:
            assert isinstance(genres, list), f"genres должен быть списком"
            for g in genres:
                assert isinstance(g, dict), f"Жанр должен быть dict, получен {type(g)}"
                assert "name" in g, "У жанра нет поля 'name'"
            genre_names = [g["name"] for g in genres]
            allure.attach(str(genre_names), name="Genres",
                           attachment_type=allure.attachment_type.TEXT)

