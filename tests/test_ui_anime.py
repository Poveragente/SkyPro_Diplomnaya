import allure
from pages.movie_page import MoviePage


@allure.epic("Кинопоиск")
@allure.feature("Поиск Анимэ")
@allure.title("Тест: поиск, Анимэ")
def test_search_and_trailer_controls(session):  # <-- Передаем фикстуру session (она содержит driver)
    driver = session
    page = MoviePage(driver)

    with allure.step("Открыть Кинопоиск"):
        page.open()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="HomePage_Open",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Закрыть рекламу"):
        try:
            page.close_ad_if_present(timeout=7)
        except Exception:
            pass

    with allure.step("Кликнуть по ANIME"):
        page.submit_anime()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="AnimePage_Loaded",
            attachment_type=allure.attachment_type.PNG,
        )
    with allure.step("Проверить карточку анимэ"):
        page.proverka_anime()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="AnimePage",
            attachment_type=allure.attachment_type.PNG,
        )