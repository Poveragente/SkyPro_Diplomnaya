import allure
from pages.movie_page import MoviePage


@allure.epic("Кинопоиск UI")
@allure.feature("Поиск и карточка фильма по описанию")
@allure.title("Тест: поиск, фильма по его описанию")
def test_search_and_trailer_controls(session):
    driver = session

    try:
        page = MoviePage(driver)

        with allure.step("Открыть Кинопоиск"):
            page.open()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="HomePage",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Закрыть рекламу"):
            page.close_ad_if_present(timeout=7)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="AfterAdClose",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Кликнуть по строке поиска"):
            search = page.click_search()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="SearchClicked",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Ввести «Фильм-погоня с трюками»"):
            page.type_movie_description(search)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="SearchFilled",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Нажать Enter"):
            page.submit_search(search)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="SearchResults",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Кликнуть на карточку фильма"):
            page.click_movie_card_descr()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="MovieCard",
                attachment_type=allure.attachment_type.PNG,
            )

    finally:
        driver.quit()
