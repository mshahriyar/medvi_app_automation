from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class AnalyzeMetabolismPage(BasePage):
    """Handles the 'Analyze Metabolism' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify 'Analyze Metabolism' content is visible")
    def verify_analyze_metabolism_content(self):
        """Verify that the 'analyze metabolism' text is visible."""
        self._retry_action(self._verify_analyze_metabolism_content)
        self.log.info("✅ Analyze metabolism content verified successfully")

    @allure.step("Click 'Next' button on Analyze Metabolism page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_analyze_metabolism_content(self):
        self.log.info("🔍 Verifying analyze metabolism content...")
        analyze_text = self.frame.locator(
            "//p[contains(normalize-space(.), 'analyze your metabolism')]"
        )
        expect(analyze_text).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
