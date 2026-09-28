import time
import allure

from pages.movie_page import MoviePage


@allure.epic("Кинопоиск")
@allure.feature("Поиск и карточка фильма")
@allure.title("Тест: поиск, карточка, управление трейлером и полноэкранным режимом")
def test_search_and_trailer_controls(session):
    driver = session
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

    with allure.step("Ввести «Джентльмены»"):
        page.type_movie_title(search)
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
        page.click_movie_card()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="MovieCard",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Прокрутить к рейтингу"):
        page.scroll_to_rating()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="RatingVisible",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Кликнуть на трейлер"):
        page.click_trailer()
        page.click_trailer_vid()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="TrailerLoaded",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Ожидаем пока пройдет реклама"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="RatingVisible",
            attachment_type=allure.attachment_type.PNG,
        )
        time.sleep(3)
