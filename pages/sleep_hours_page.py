from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class SleepHoursPage(BasePage):
    """Handles the 'Sleep Hours' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify sleep hours question and image are visible")
    def verify_sleep_heading_and_image(self):
        """Verify that the question text and image are visible."""
        self._retry_action(self._verify_sleep_heading_and_image)
        self.log.info("✅ Sleep heading and image verified")

    @allure.step("Select sleep hours option")
    def select_sleep_hours(self, sleep_hours: str):
        """Select a sleep hours option dynamically."""
        self._retry_action(lambda: self._select_sleep_hours(sleep_hours))
        self.log.info(f"✅ Selected sleep hours option: {sleep_hours}")

    @allure.step("Click 'Next' button on Sleep Hours page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_sleep_heading_and_image(self):
        self.log.info("🔍 Verifying sleep heading and image...")
        sleep_heading = self.frame.locator(
            "//*[normalize-space(text())='How many hours of sleep do you usually get each night?']"
        )
        sleep_image = self.frame.locator(
            "img[src*='id-1tAZd12DZCus/widgetid-k1Xy/hHZFcPL7X59pJZtoxUx5JW/gallaghergallagher_Romantic_lifestyle_photography_style_warm__cdfcbe67-e11e-45d2-8ef5-2f0a6d85ca4c_3.png']"
        )
        expect(sleep_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(sleep_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_sleep_hours(self, sleep_hours: str):
        self.log.info(f"😴 Selecting sleep hours option: {sleep_hours}")
        safe_value = self.escape_xpath_text(sleep_hours)
        locator_str = f"//div[normalize-space(text())={safe_value}]"
        sleep_option = self.frame.locator(locator_str)
        sleep_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        sleep_option.scroll_into_view_if_needed()
        expect(sleep_option).to_be_visible(timeout=5000)
        sleep_option.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
