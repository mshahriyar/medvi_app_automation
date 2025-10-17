from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class LoseWeightPage(BasePage):
    """Handles the 'Lose Weight' step in the MEDVi Typeform flow."""

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
    @allure.step("Verify lose weight heading")
    def verify_lose_weight_heading(self):
        """Verify that the lose weight heading text is visible."""
        self._retry_action(self._verify_lose_weight_heading)
        self.log.info("✅ Lose weight heading visible")

    @allure.step("Select lose weight option")
    def select_lose_weight(self, lose_weight_value: str):
        """Select an option for how fast the user wants to lose weight."""
        self._retry_action(lambda: self._select_lose_weight(lose_weight_value))
        self.log.info(f"✅ Selected lose weight option: {lose_weight_value}")

    @allure.step("Click 'Next' button on Lose Weight page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_lose_weight_heading(self):
        self.log.info("🔍 Verifying lose weight heading...")
        heading = self.frame.locator(
            "//*[normalize-space(text())='How is that pace for you?']"
        )
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_lose_weight(self, lose_weight_value: str):
        self.log.info(f"⚖️ Selecting lose weight option: {lose_weight_value}")
        safe_value = self.escape_xpath_text(lose_weight_value)
        locator_str = f"//div[normalize-space(text())={safe_value}]"
        option = self.frame.locator(locator_str)
        option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option.scroll_into_view_if_needed()
        expect(option).to_be_visible(timeout=5000)
        option.click()

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
