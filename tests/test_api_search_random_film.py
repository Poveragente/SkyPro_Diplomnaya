import os
import json
import time
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
@allure.story("Поиск рандомного фильма")
@pytest.mark.api
def test_find_random_movie(api):

    # ── Шаг 1. Получение рандомного фильма ──
    with allure.step("Запрос рандомного фильма"):
        start_time = time.time()
        movie = api.get_random_movie()
        elapsed = time.time() - start_time

        allure.attach(f"{elapsed:.3f}s", name="Response Time",
                       attachment_type=allure.attachment_type.TEXT)
        assert elapsed < 5.0, f"Ответ занял {elapsed:.2f}s, порог 5s"

        _attach_json("Random Movie", movie)

        # Ответ должен быть dict (один фильм, не список)
        assert isinstance(movie, dict), (
            f"Ожидался dict, получен {type(movie)}"
        )

    # ── Шаг 2. Проверка обязательных полей ──
    with allure.step("Проверка обязательных полей"):
        assert "id" in movie, "У фильма нет поля 'id'"
        assert isinstance(movie["id"], int), (
            f"id должен быть int, получен {type(movie['id'])}"
        )
        allure.attach(str(movie["id"]), name="Random Film ID",
                       attachment_type=allure.attachment_type.TEXT)

        assert "type" in movie, "У фильма нет поля 'type'"
        assert isinstance(movie["type"], str), (
            f"type должен быть str, получен {type(movie['type'])}"
        )
        assert movie["type"], "type не должен быть пустым"
        allure.attach(movie["type"], name="Film Type",
                       attachment_type=allure.attachment_type.TEXT)

        # Хотя бы одно имя должно быть
        name = movie.get("name", "")
        alt_name = movie.get("alternativeName", "")
        en_name = movie.get("enName", "")
        assert name or alt_name or en_name, (
            "Все поля имени пустые (name, alternativeName, enName)"
        )
        display_name = name or alt_name or en_name
        allure.attach(display_name, name="Film Name",
                       attachment_type=allure.attachment_type.TEXT)

    # ── Шаг 3. Проверка рандомности (два запроса дают разные фильмы) ──
    with allure.step("Проверка рандомности — повторный запрос"):
        movie2 = api.get_random_movie()
        _attach_json("Random Movie #2", movie2)

        assert "id" in movie2, "У второго фильма нет поля 'id'"
        allure.attach(str(movie2["id"]), name="Random Film #2 ID",
                       attachment_type=allure.attachment_type.TEXT)

        # Вероятность совпадения крайне мала, но не нулевая
        # Если совпало — делаем третий запрос
        if movie["id"] == movie2["id"]:
            movie3 = api.get_random_movie()
            _attach_json("Random Movie #3", movie3)
            allure.attach(
                f"Первые два совпали (ID={movie['id']}), "
                f"третий ID={movie3.get('id')}",
                name="Randomness Check",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert movie3["id"] != movie["id"], (
                "Три подряд рандомных запроса вернули один и тот же ID — "
                "рандомность под вопросом"
            )
        else:
            allure.attach(
                f"Два разных ID: {movie['id']} и {movie2['id']} — рандом работает",
                name="Randomness Confirmed",
                attachment_type=allure.attachment_type.TEXT,
            )

    # ── Шаг 4. Проверка структуры вложенных полей ──
    with allure.step("Проверка вложенных полей (рейтинг, жанры, год)"):
        # Год
        year = movie.get("year")
        if year is not None:
            assert isinstance(year, int), f"year должен быть int, получен {type(year)}"

        # Рейтинг
        rating = movie.get("rating", {})
        if isinstance(rating, dict):
            for key in ("kp", "imdb"):
                val = rating.get(key)
                if val is not None:
                    assert isinstance(val, (int, float)), (
                        f"rating.{key} должен быть числом, получен {type(val)}"
                    )
                    assert 0 <= val <= 10, (
                        f"rating.{key}={val} вне диапазона 0-10"
                    )

        # Жанры
        genres = movie.get("genres", [])
        if genres:
            assert isinstance(genres, list), "genres должен быть списком"
            for g in genres:
                assert isinstance(g, dict), f"Жанр должен быть dict, получен {type(g)}"
                assert "name" in g, "У жанра нет поля 'name'"

        # Страны
        countries = movie.get("countries", [])
        if countries:
            assert isinstance(countries, list), "countries должен быть списком"
            for c in countries:
                assert isinstance(c, dict), f"Страна должна быть dict, получен {type(c)}"
                assert "name" in c, "У страны нет поля 'name'"