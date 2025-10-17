from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class ReasonsPage(BasePage):
    """Handles reasons selection in the MEDVi Typeform flow."""

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

    @allure.step("Verify reasons heading is visible")
    def verify_reasons_heading_visible(self):
        """Verify the reasons heading is visible."""
        self._retry_action(self._verify_reasons_heading)
        self.log.info("✅ Reasons heading verified successfully")

    @allure.step("Select reason for weight loss")
    def select_reason(self, reason: str):
        """Select a reason for weight loss."""
        self._retry_action(lambda: self._select_reason(reason))
        self.log.info(f"✅ Reason selected: {reason}")

    @allure.step("Click 'Next' button on Reasons page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_reasons_heading(self):
        self.log.info("🔍 Verifying reasons heading...")
        heading = self.frame.locator("//span[contains(text(), 'Improving your life requires ')]")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_reason(self, reason: str):
        self.log.info(f"🎯 Selecting reason: {reason}")
        safe_value = self.escape_xpath_text(reason)
        reason_locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")
        reason_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        reason_locator.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
