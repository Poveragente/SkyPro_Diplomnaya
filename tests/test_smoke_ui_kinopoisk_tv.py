import allure
from selenium.webdriver.support import expected_conditions as EC
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

    with allure.step("Проверить наличие карточек каналов"):
        cards = page.wait.until(
            EC.visibility_of_any_elements_located(page.FIRST_CHANNEL_CARD)
        )
        assert (
            len(cards) >= 1
        ), f"Не найдено ни одной карточки канала. Найдено: {len(cards)}"

    with allure.step("Сделать скриншот списка каналов"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="FederalChannelsList",
            attachment_type=allure.attachment_type.PNG,
        )
