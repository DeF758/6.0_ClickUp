import os
import sys


# Добавляем корневую директорию проекта в пути импорта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import pytest
import allure
from playwright.sync_api import sync_playwright
from items.board_ui_items import BoardUiItems
from items.login_ui_items import LoginUiItems
from src.api.clickup_api import ClickupApi
from src.data.task_model import TaskModel
from src.scenarios.scenarios import clear_board, create_and_get_task_id, create_and_get_task_name
from utils.helpers import Helper


@pytest.fixture(scope="session")
def auth_sess():
    client = ClickupApi()
    return client


@allure.title("Генерация данных для всех полей")
@pytest.fixture(scope="function")
def get_gen_data():
    return TaskModel.gen_fake_data()


@allure.title("Генерация данных для обязательного поля")
@pytest.fixture(scope="function")
def get_gen_req_field():
    return TaskModel.gen_required_field()


@allure.title("Создание задачи и получение task_id")
@pytest.fixture(scope="function")
def get_task_id(auth_sess, get_gen_data):
    return create_and_get_task_id(auth_sess, get_gen_data)

@allure.title("Создание задачи и получение name")
@pytest.fixture(scope="function")
def get_task_name(auth_sess, get_gen_data):
    return create_and_get_task_name(auth_sess, get_gen_data)


@allure.title("Очистка доски")
@pytest.fixture(scope="class", autouse=True)
def clear_tasks(auth_sess):
    data_id = auth_sess.get_tasks().json()["tasks"]
    data_id_archived = auth_sess.get_tasks(archived="true").json()["tasks"]
    ids = [task_id["id"] for task_id in data_id]
    ids += [task_id["id"] for task_id in data_id_archived]
    clear_board(auth_sess, *ids)
    yield
    data_id = auth_sess.get_tasks().json()["tasks"]
    data_id_archived = auth_sess.get_tasks(archived="true").json()["tasks"]
    ids = [task_id["id"] for task_id in data_id]
    ids += [task_id["id"] for task_id in data_id_archived]
    clear_board(auth_sess, *ids)

@allure.title("Запуск браузера")
@pytest.fixture(scope="function")
def browser():
    plwrght = sync_playwright().start()
    run_browser = plwrght.chromium.launch(headless=False)
    yield run_browser
    run_browser.close()
    plwrght.stop()

@allure.title("Создание объекта страницы авторизации")
@pytest.fixture(scope="function")
def browse_login_page(browser):
    return LoginUiItems(browser.new_page())

@allure.title("Создание объекта страницы доски")
@pytest.fixture(scope="function")
def browse_board_page(browse_login_page, ui_auth):
    return BoardUiItems(browse_login_page.page)

@allure.title("Авторизация через UI")
@pytest.fixture(scope="function")
def ui_auth(browse_login_page):
    login_page = browse_login_page
    login_page.login_success(Helper.EMAIL, Helper.PASSWORD)
