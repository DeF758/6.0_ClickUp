from enum import Enum

from playwright.sync_api import Locator

from items.general_ui_items import GeneralUiItems


class LoginSelector(Enum):
    EMAIL = "login-email-input"
    PASSWORD = "login-password-input"
    LOG_IN = "login-submit"


class LoginUiItems(GeneralUiItems):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = ""

    def input_field(self, field_name: LoginSelector) -> Locator:
        return self.page.locator(f"#{field_name.value}")

    def input_field_err(self, field_name: LoginSelector) -> Locator:
        return self.page.locator(f"//*[@id='{field_name.value}']/../../p")

    def button(self, button_name: LoginSelector) -> Locator:
        return self.page.locator(f"//button[@data-test='{button_name.value}']")

    def go_to_login_page(self):
        self.navigate_to(self._get_full_url)

    def login_success(self, lgn, psswrd):
        self.navigate_to(self._get_full_url)
        self.input_field(LoginSelector.EMAIL).fill(lgn)
        self.input_field(LoginSelector.PASSWORD).fill(psswrd)
        self.button(LoginSelector.LOG_IN).click()
        self.assert_text_present_page("Home")
