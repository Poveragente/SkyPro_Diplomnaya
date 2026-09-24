import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.movie_page import MoviePage

@allure.epic("Кинопоиск")
@allure.feature("Поиск Анимэ")
@allure.title("Тест: поиск, Анимэ")
def test_search_and_trailer_controls():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

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

    with allure.step("Кликнуть по ANIME"):
        page.submit_anime()
        allure.attach(
                driver.get_screenshot_as_png(),
                name="HomePage",
                attachment_type=allure.attachment_type.PNG,
            )

