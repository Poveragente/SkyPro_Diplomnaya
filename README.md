# Автотесты для Кинопоиска (дипломный проект)

Проект реализует автоматизацию UI и API тестирования сайта Кинопоиск.
Для UI тестов используются классы обьектов page movie_page и kinopoisk_tv_page
там указаны основные методы и селекторы для работы тестов
Для API тестов используется библиотека api_class_page там указаны основные методы для работы тестов
в файле conftest.py - написаны фикстуры для работы с проектом

## Технологии
Python 3.11+
selenium==4.25.0
requests==2.32.3
pytest==8.3.3
allure-pytest==3.1.9
python-dotenv==1.0.1
webdriver-manager==4.0.0

Указаны в файле зависимостей в requirements.txt

## Установка
```bash
pip install -r requirements.txt

## Установка ключей 
	1. Для начала вам необходимо создать файл с расширением .env
	2. Открыть его в текстовом редакторе и заполнить следующими полями

		BASE_URL=https://api.poiskkino.dev
		API_BASE_URL=https://api.poiskkino.dev
		API_KEY=XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX
		TIMEOUT=30
		HEADLESS=false

	3. Сохранить

API_KEY можно получить через Телеграмм Бота перейдя по ссылке https://poiskkino.dev/
и нажав на кнопку Получить API(необходимо делать с включенным VPN так как ТГ на территории РФ заблокирован)

