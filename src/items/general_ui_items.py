from playwright.sync_api import expect, Page

from enums.urls import Url


class GeneralUiItems:
    def __init__(self, page: Page):
        self.page = page
        self._endpoint = ""

    @property
    def _get_full_url(self):
        return f"{Url.UI_URL.value.rstrip("/")}/{self._endpoint.lstrip("/")}"

    @_get_full_url.setter
    def _get_full_url(self, endpoint):
        self._endpoint = endpoint

    def navigate_to(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("load")

    def wait_for_selector_and_click(self, selector):
        self.page.wait_for_selector(selector)
        self.page.click(selector)

    def wait_for_selector_and_fill(self, selector, value):
        self.page.wait_for_selector(selector.value)
        self.page.fill(selector.value, value)  # заменяет текст вставкой

    def wait_for_selector_and_type(self, selector, value, delay):
        self.page.wait_for_selector(selector.value)
        self.page.type(selector.value, value, delay=delay)  # дополняет текст вводом (скорость ввода delay)

    def assert_element_visible(self, selector):
        expect(self.page.locator(selector)).to_be_visible()

    def assert_text_present_page(self, text, timeout: int = 30000):
        expect(self.page.locator("body")).to_contain_text(text, timeout=timeout)

    def assert_text_element(self, selector, text):
        expect(self.page.locator(selector)).to_have_text(text)

    def assert_input_value(self, selector, expected_value):
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def wait_for_app_stable(self):
        self.page.wait_for_function(
            """() => new Promise(resolve => {
                let last = performance.now();
                function check() {
                    const now = performance.now();
                    if (now - last > 300) resolve(true);
                    last = now;
                    requestAnimationFrame(check);
                }
                requestAnimationFrame(check);
            })"""
        )
