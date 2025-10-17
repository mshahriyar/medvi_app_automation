from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class RankPage(BasePage):
    """Handles the Rank verification step in the MEDVi Typeform flow."""

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

    @allure.step("Verify rank content is visible")
    def verify_rank_content_visible(self):
        """Verify the rank content is visible."""
        self._retry_action(self._verify_rank_content_visible)
        self.log.info("✅ Rank content is visible verified successfully")

    @allure.step("Verify Forbes rank image is visible")
    def verify_rank(self):
        """Verify that the Forbes #1 rank image is displayed."""
        self._retry_action(self._verify_rank)
        self.log.info("✅ Rank image verified successfully")

    @allure.step("Click 'Next' button on Rank page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_rank_content_visible(self):
        self.log.info("🔍 Verifying rank content is visible...")
        content = self.frame.locator("//*[normalize-space(text())='ranked #1']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _verify_rank(self):
        self.log.info("🏆 Verifying Forbes rank image visibility...")
        rank_image = self.frame.locator("img[src*='forbes-number-1.png']")
        rank_image.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        expect(rank_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
