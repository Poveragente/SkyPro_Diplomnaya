import allure
from pages.kinopoisk_tv_page import KinopoiskTvPage


@allure.epic("Кинопоиск")
@allure.feature("Телеканалы")
@allure.title("Проверка отображения списка федеральных каналов")
def test_federal_channels_display(driver):
    page = KinopoiskTvPage(driver)

    with allure.step("Открыть Кинопоиск"):
        page.open_fullscreen()

    with allure.step("Закрыть рекламу"):
        page.close_ad_if_present(timeout=7)

    with allure.step("Перейти в раздел «Телеканалы»"):
        page.click_tv_channels()

    with allure.step("Выбрать вкладку «Федеральные»"):
        page.click_federal_tab()

    with allure.step("Сделать скриншот списка каналов"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="FederalChannelsList",
            attachment_type=allure.attachment_type.PNG,
        )

