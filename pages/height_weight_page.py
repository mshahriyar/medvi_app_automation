from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage

class HeightWeightPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=2):
        """Retry a flaky action several times before giving up."""
        for attempt in range(1, retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt < retries:
                    self.log.warning(f"🔁 Attempt {attempt}/{retries} failed: {e}. Retrying in {delay}s…")
                    time.sleep(delay)
                else:
                    self.log.error(f"❌ All {retries} attempts failed: {e}")
                    raise

    @allure.step("Wait for Typeform iframe to load")
    def wait_for_iframe_ready(self, max_retries: int = 5):
        """Wait for the Typeform iframe to fully load (and the first control is visible)."""
        self.log.info("🔄 Waiting for iframe to load...")

        for attempt in range(1, max_retries + 1):
            try:
                # 1) Ensure iframe element is present
                self.page.wait_for_selector(
                    self.IFRAME_SELECTOR, state="attached", timeout=self.DEFAULT_TIMEOUT
                )

                # 2) Ensure a known control inside iframe is visible (feet dropdown)
                feet_input = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
                feet_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)

                self.log.info("✅ Iframe loaded and first control visible")
                return
            except Exception as e:
                self.log.warning(f"⚠️ Iframe not ready (Attempt {attempt}/{max_retries}): {e}")
                if attempt < max_retries:
                    # Light recovery: reload page (or you could reassign iframe src)
                    self.page.reload()
                    time.sleep(3)
                else:
                    raise TimeoutError("❌ Iframe failed to load after multiple retries.") from e

    # ----------------------- Form Actions -----------------------

    @allure.step("Select feet")
    def select_feet(self, value: str):
        """Select feet value."""
        self._retry_action(lambda: self._select_dropdown(1, value))
        self.log.info(f"✅ Selected feet: {value}")

    @allure.step("Select inches")
    def select_inches(self, value: str):
        """Select inches value."""
        self._retry_action(lambda: self._select_dropdown(2, value))
        self.log.info(f"✅ Selected inches: {value}")

    @allure.step("Enter weight")
    def add_weight(self, weight: str):
        """Enter the user's weight."""
        self._retry_action(lambda: self._fill_input(weight))
        self.log.info("✅ Weight entered successfully")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _select_dropdown(self, position: int, value: str):
        dropdown = self.frame.locator(f"(//div[@data-cy='dropdown-component'])[{position}]//input")
        dropdown.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        dropdown.click()
        dropdown.fill(value)
        self.page.keyboard.press("Enter")

    def _fill_input(self, value: str):
        weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        weight_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        weight_input.fill(value)
        expect(weight_input).to_have_value(value, timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
