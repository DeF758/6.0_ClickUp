import pytest
import allure

from src.api.clickup_api import ClickupApi
from src.data.task_model import TaskModel
from src.scenarios.scenarios import  clear_board


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

@allure.title("Очистка доски")
@pytest.fixture(scope="session",autouse=True)
def clear_tasks(auth_sess):
    data_id = auth_sess.get_tasks().json()["tasks"]
    data_id_archived = auth_sess.get_tasks(archived="true").json()["tasks"]
    ids = [task_id["id"] for task_id in data_id]
    ids += [task_id["id"] for task_id in data_id_archived]
    clear_board(auth_sess, *ids)
    yield


