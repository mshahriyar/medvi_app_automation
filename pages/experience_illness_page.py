from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class ExperienceIllnessPage(BasePage):
    """Handles 'Experience Illness' step interactions in the MEDVi Typeform flow."""

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
    @allure.step("Verify experience illness content is visible")
    def verify_experience_illness_content_visible(self):
        """Verify the experience illness content is visible."""
        self.log.info("🔍 Verifying experience illness content is visible...")
        content = self.frame.locator("//*[normalize-space(text())='Do you experience any of the following?']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Experience illness content is visible verified successfully")

    @allure.step("Select experience illness option")
    def select_experience_illness(self, experience_illness_value: str):
        """Select an illness option dynamically based on provided value."""
        self._retry_action(lambda: self._select_experience_illness(experience_illness_value))
        self.log.info(f"✅ Successfully selected: '{experience_illness_value.strip()}'")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _select_experience_illness(self, experience_illness_value: str):
        clean_value = experience_illness_value.strip()
        self.log.info(f"🩺 Selecting experience illness: '{clean_value}'")

        safe_value = self.escape_xpath_text(clean_value)
        option_locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")

        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        expect(option_locator).to_be_visible(timeout=5000)
        option_locator.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()

