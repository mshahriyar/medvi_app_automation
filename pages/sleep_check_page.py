from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class SleepCheckPage(BasePage):
    """Handles the 'Sleep Check' step in the MEDVi Typeform flow."""

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

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify sleep routine heading is visible")
    def verify_sleep_routine_heading_visible(self):
        """Verify that the sleep routine heading is visible."""
        self._retry_action(self._verify_sleep_routine_heading)
        self.log.info("✅ Sleep routine heading visible")

    @allure.step("Select sleep routine option")
    def select_sleep_routine(self, sleep_value: str):
        """Select a sleep routine option (handles quotes safely)."""
        self._retry_action(lambda: self._select_sleep_routine(sleep_value))
        self.log.info(f"✅ Selected sleep routine: {sleep_value}")

    @allure.step("Click 'Next' button on Sleep Check page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_sleep_routine_heading(self):
        self.log.info("🔍 Verifying sleep routine heading...")
        heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'How you sleep tells us a lot about your')]"
        )
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_sleep_routine(self, sleep_value: str):
        self.log.info(f"😴 Selecting sleep routine: {sleep_value}")
        quote = '"' if "'" in sleep_value else "'"
        locator_str = f"//div[normalize-space(text())={quote}{sleep_value}{quote}]"
        sleep_option = self.frame.locator(locator_str)
        sleep_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        sleep_option.scroll_into_view_if_needed()
        expect(sleep_option).to_be_visible(timeout=5000)
        sleep_option.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
