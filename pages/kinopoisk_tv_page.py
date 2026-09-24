import allure
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class KinopoiskTvPage:
    # --- Локаторы ---
    TV_CHANNELS_LINK = (By.XPATH, '//nav//a[contains(., "Телеканалы")]')
    FEDERAL_TAB = (By.XPATH, '//button[contains(., "Федеральные")]')
    FIRST_CHANNEL_CARD = (By.CSS_SELECTOR, 'div[class*="styles_container"]')
    CLOSE_AD_BUTTON = (
        By.CSS_SELECTOR,
        'button svg path[d^="m12.666"], a svg path[d^="m12.666"]',
    )

    def __init__(self, driver, url="https://www.kinopoisk.ru"):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)

    @allure.step("Открытие браузера и переход на kinopoisk.ru")
    def open_fullscreen(self) -> None:
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @allure.step("Закрыть баннер-рекламу (если есть)")
    def close_ad_if_present(self, timeout=5) -> bool:
        """Закрыть рекламу. Возвращает True, если закрыл."""
        for locator in [self.CLOSE_AD_BUTTON]:
            try:
                btn = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                btn.click()
                return True
            except Exception:
                continue
        return False

    @allure.step("Клик по разделу «Телеканалы»")
    def click_tv_channels(self) -> None:
        link = self.wait.until(EC.element_to_be_clickable(self.TV_CHANNELS_LINK))
        link.click()

    @allure.step("Клик по вкладке «Федеральные»")
    def click_federal_tab(self) -> None:
        federal = self.wait.until(EC.element_to_be_clickable(self.FEDERAL_TAB))
        federal.click()
        self.wait.until(EC.visibility_of_element_located(self.FIRST_CHANNEL_CARD))
