from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class FrankNewManPage(BasePage):
    """Handles testimonial verification in the MEDVi Typeform flow."""

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

    @allure.step("Verify testimonial text is visible")
    def verify_recommendation_visible(self):
        """Verify that the testimonial text is visible inside the iframe."""
        self._retry_action(self._verify_recommendation)
        self.log.info("✅ Testimonial text verified successfully")

    @allure.step("Click 'Next' button on testimonial page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_recommendation(self):
        self.log.info("🔍 Verifying testimonial visibility...")
        # Combine both locators (h2 + p) into one
        recommendation_locator = self.frame.locator(
            "//h2[contains(@class, 'ql-align-center')] | //p[contains(@class, 'ql-align-center')]"
        )
        # Wait for visibility
        expect(recommendation_locator.first).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
