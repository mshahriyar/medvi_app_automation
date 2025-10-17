from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class BodyReviewPage(BasePage):
    """Handles the 'Body Review' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify Body Review content")
    def verify_body_review_content(self):
        """Verify that the heading and image are visible on the Body Review page."""
        self._retry_action(self._verify_body_review_content)
        self.log.info("✅ Body Review heading and image verified successfully")

    @allure.step("Click 'Next' button on Body Review page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_body_review_content(self):
        self.log.info("🔍 Verifying Body Review content...")
        heading = self.frame.locator(
            "//h2[contains(@class, 'ql-align-center')]"
        )
        text_content = self.frame.locator(
            "//p[contains(@class, 'ql-align-center')]"
        )
        image = self.frame.locator("img[src*='/13.png']")
        expect(text_content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
