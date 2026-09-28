import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MoviePage:
    """Page Object для страницы фильма на Кинопоиске."""

    # --- Локаторы ---
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.kinopoisk-header-search-form-input__input")
    SEARCH_RESULTS = (
        By.CSS_SELECTOR,
        "div[class*='list-item'], div[class*='card-container'], a[data-test-id='next-link']",
    )
    MOVIE_CARD = (By.XPATH, "//span[contains(text(), 'Джентльмены')]/ancestor::a[1]")
    MOVIE_CARD_DESCR = (By.CSS_SELECTOR,
    "[class*='base-movie-main-info_link']")
    POSTER = (By.CSS_SELECTOR, ".film-poster, .poster")
    RATING_BLOCK = (
        By.XPATH,
        "//*[contains(., 'Рейтинг')] | //*[contains(@class, 'rating')]",
    )
    ACTOR_CARD = (By.XPATH,"//a[@id='suggest-item-person-20303']")

    TRAILER_BTN = (By.CSS_SELECTOR, "a[data-tid='23a2a59']")
    TRAILER_EMBED = (
        By.CSS_SELECTOR,
        "div[data-trailer-id='214191'] .js-kinopoisk-widget-embed",
    )
    CLOSE_AD_BUTTON = (By.CSS_SELECTOR, "button svg path[d^='m12.666']")

    ANIME = (By.XPATH, '//nav//a[contains(., "Аниме")]')

    ANIME_CARD = (By.CSS_SELECTOR, 'a[data-test-id="RouterLink"]')


    def __init__(self, driver, url="https://www.kinopoisk.ru", timeout: int = 15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # --- Открытие страницы ---
    @allure.step("Открыть https://www.kinopoisk.ru")
    def open(self) -> None:
        self.driver.get("https://www.kinopoisk.ru")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # --- Реклама ---
    @allure.step("Закрыть баннер-рекламу (если есть)")
    def close_ad_if_present(self, timeout: int = 5) -> bool:
        """закрыть рекламу. Возвращает True, если закрыл."""
        try:
            path_elem = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.CLOSE_AD_BUTTON)
            )
            parent = self.driver.execute_script(
                "return arguments[0].parentElement;", path_elem
            )
            parent.click()
            return True
        except Exception:
            return False
    # --- Поиск ---
    @allure.step("Кликнуть по строке поиска")
    def click_search(self) -> WebElement:
        search = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        search.click()
        return search
    # --- Ввод названия фильма ---
    @allure.step("Ввести название фильма «Джентльмены»")
    def type_movie_title(self, search: WebElement, title: str = "Джентльмены") -> None:
        search.clear()
        search.send_keys(title)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value").strip()
            == title
        )
    # --- Ввод описания фильма ---
    @allure.step("Ввести descriptions фильма ")
    def type_movie_description(self, search: WebElement, title: str = "Фильм-погоня с трюками»") -> None:
        search.clear()
        search.send_keys(title)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value").strip()
            == title
        )
    # --- Ввод имени актрисы ---
    @allure.step("Ввести имя актрисы «Николь Кидман»")
    def type_actrees_title(self, search: WebElement, title: str = "Николь Кидман") -> None:
        search.clear()
        search.send_keys(title)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value").strip()
            == title
        )
    # Нажатие кнопки Ввод
    @allure.step("Нажать Enter в строке поиска и дождаться результатов")
    def submit_search(self, search: WebElement) -> None:
        search.send_keys(Keys.ENTER)
        # Исправленное ожидание: ждём хотя бы один видимый результат
        self.wait.until(
            lambda d: len(d.find_elements(*self.SEARCH_RESULTS)) > 0
        )
    # Нажатие кнопки ANIME
    @allure.step("Кликнуть по кнопке Анимэ")
    def submit_anime(self) -> None:
        btn = self.driver.find_element(*self.ANIME)
        btn.click()
    # --- Карточка фильма ---
    @allure.step("Кликнуть на карточку фильма по data-test-id")
    def click_movie_card(self) -> None:
        # Ждем, пока ссылка станет кликабельной
        card_link = self.wait.until(EC.element_to_be_clickable(self.MOVIE_CARD))
        card_link.click()

        # Ждем появления элементов страницы фильма (например, постера)
        self.wait.until(EC.presence_of_element_located(self.POSTER))

    @allure.step("Кликнуть на карточку фильма")
    def click_movie_card_descr(self) -> None:
        # Ждем, пока ссылка станет кликабельной
        card_link = self.wait.until(EC.element_to_be_clickable(self.MOVIE_CARD_DESCR))
        card_link.click()

        # Ждем появления элементов страницы фильма (например, постера)
        self.wait.until(EC.presence_of_element_located(self.POSTER))

    @allure.step("Кликнуть на карточку актрисы")
    def click_actrees_card(self) -> None:
        # Ждем, пока ссылка станет кликабельной
        card_link = self.wait.until(EC.element_to_be_clickable(self.ACTOR_CARD))
        card_link.click()

    # --- Скролл к рейтингу ---
    @allure.step("Прокрутить страницу к рейтингу")
    def scroll_to_rating(self) -> None:
        rating = self.wait.until(EC.presence_of_element_located(self.RATING_BLOCK))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", rating
        )
        self.wait.until(EC.visibility_of(rating))

    # --- переход на страницу с трейлером---
    @allure.step("Кликнуть на widget")
    def click_trailer(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.TRAILER_BTN))
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".styles_fade_UKtdM"))
        )
        btn = self.wait.until(EC.element_to_be_clickable(self.TRAILER_BTN))
        btn.click()

    # --- Показ трейлера ---
    @allure.step("Кликнуть на трейлер")
    def click_trailer_vid(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.TRAILER_EMBED))
        el = self.driver.find_element(*self.TRAILER_EMBED)
        el.click()

    @allure.step("Проверка карточки АНИМЭ")
    def proverka_anime(self) -> None:
        self.wait.until(EC.presence_of_element_located(self.ANIME_CARD))


