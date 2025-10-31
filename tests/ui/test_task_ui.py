import allure
from playwright.sync_api import expect

from items.board_ui_items import BoardSelector
from items.login_ui_items import LoginSelector
from utils.helpers import Helper


@allure.feature("UI Tests")
class TestTaskUi:
    @allure.title("Успешная авторизация")
    def test_login_success(self, browse_login_page):
        with allure.step("Подготовка окружения"):
            login_page = browse_login_page
        with allure.step("Успешная авторизация и проверка редиректа на главную страницу"):
            login_page.login_success(Helper.EMAIL, Helper.PASSWORD)

    @allure.title("Авторизация с неправильным паролем")
    def test_login_negative(self, browse_login_page):
        with allure.step("Подготовка окружения"):
            login_page = browse_login_page
        with allure.step("Открыть страницу авторизации"):
            login_page.go_to_login_page()
        with allure.step("Заполнить поле 'Email' валидными данными"):
            login_page.input_field(LoginSelector.EMAIL).fill(Helper.EMAIL)
        with allure.step("Заполнить поле 'Password' не валидными данными"):
            login_page.input_field(LoginSelector.PASSWORD).fill("admin1234")
        with allure.step("Нажать кнопку 'Log In'"):
            login_page.button(LoginSelector.LOG_IN).click()
        with allure.step("Проверить отображение ошибки о некорректном пароле"):
            expect(login_page.input_field_err(LoginSelector.PASSWORD).filter(has_text="Incorrect password for this email."))

    @allure.title("Удаление задачи")
    def test_delete_task(self, browse_board_page, get_task_name):
        with allure.step("Подготовка окружения"):
            board_page = browse_board_page
        with allure.step("Создать задачу через API"):
            task_name = get_task_name
        with allure.step("Открыть страницу с доской"):
            board_page.go_to_board_page()
        with allure.step("Открыть задачу"):
            board_page.task_button(task_name).click()
        with allure.step("Открыть настройки задачи"):
            board_page.button(BoardSelector.TASK_SETTINGS).click()
        with allure.step("Удалить задачу"):
            board_page.button(BoardSelector.DELETE).click()
        with allure.step("Проверить, что задача удалена"):
            expect(board_page.task_button(task_name)).not_to_be_attached()

    @allure.title("Создание задачи")
    def test_create_task(self, browse_board_page, get_gen_data):
        with allure.step("Подготовка окружения"):
            board_page = browse_board_page
        with allure.step("Открыть страницу с доской"):
            board_page.go_to_board_page()
        with allure.step("Нажать '+ Add Task'"):
            board_page.add_task_in_status().click()
        with allure.step("Заполнить название задачи"):
            board_page.input_field(BoardSelector.TASK_NAME_FIELD).type(get_gen_data.name, delay=10)
        with allure.step("Нажать 'Save'"):
            board_page.button(BoardSelector.CREATE_TASK).click()
        with allure.step("Проверить, что задача создана"):
            expect(board_page.task_button(get_gen_data.name)).to_be_visible()
