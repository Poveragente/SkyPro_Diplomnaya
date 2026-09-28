import allure
from pages.movie_page import MoviePage


@allure.epic("Кинопоиск")
@allure.feature("Поиск актрисы")
@allure.title("Тест: поиск, карточка")
def test_search_actrees(session):
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

    with allure.step("Ввести «Николь Кидман»"):
        page.type_actrees_title(search)
        allure.attach(
            driver.get_screenshot_as_png(),
            name="SearchFilled",
            attachment_type=allure.attachment_type.PNG,
        )
    with allure.step("Кликнуть на карточку актрисы"):
        page.click_actrees_card()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="ActorCardOpened",
            attachment_type=allure.attachment_type.PNG,
        )

