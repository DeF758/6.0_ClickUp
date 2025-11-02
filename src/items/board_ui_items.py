from enum import Enum

from playwright.sync_api import Locator

from items.general_ui_items import GeneralUiItems


class BoardSelector(Enum):
    SEARCH_LINE = "command-bar__input"
    SEARCH_BTTN = "search-modal-toggle__search-modal"
    TASK_SETTINGS = "task-view-header__task-settings"
    DELETE = "dropdown-list-item__cu-task-view-menu-delete"
    INITIALIZING_TASK_CREATION="board-group__create-task-button__Add Task"
    CREATE_TASK="quick-create-task-panel__panel-board__enter-button"
    TASK_NAME_FIELD="quick-create-task-panel__panel-board__input"


class BoardUiItems(GeneralUiItems):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "/90151520308/v/b/t/90151520308"

    def go_to_board_page(self):
        self.navigate_to(self._get_full_url)

    def input_field(self, field_name: BoardSelector) -> Locator:
        return self.page.locator(f"//input[@data-test='{field_name.value}']")

    def button(self, field_name: BoardSelector) -> Locator:
        return self.page.locator(f"//button[@data-test='{field_name.value}']")

    def task_button(self, task_name: str) -> Locator:
        return self.page.locator(f"//button[.//span[text()=' Open {task_name} ']]")

    def add_task_in_status(self)->Locator:
        return self.page.locator(f"//li[1]//button[@data-test='board-group__create-task-button__Add Task']")
