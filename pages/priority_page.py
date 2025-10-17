from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class PriorityPage(BasePage):
    """Handles 'Priority' step interactions in the MEDVi Typeform flow."""

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

    # ----------------------   Actions ---------------------- #

    @allure.step("Verify priority content is visible")
    def verify_priority_content_visible(self):
        """Verify the priority content is visible."""
        self._retry_action(self._verify_priority_content_visible)
        self.log.info("✅ Priority content is visible verified successfully")

    @allure.step("Select user goal priority")
    def select_goal(self, goal_value: str):
        """Selects a goal (Lose Weight / Gain Muscle / Maintain)."""
        self._retry_action(lambda: self._select_goal(goal_value))
        self.log.info(f"✅ Selected goal: {goal_value}")

    @allure.step("Click 'Next' button on Priority page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_priority_content_visible(self):
        self.log.info("🔍 Verifying priority content is visible...")
        content = self.frame.locator("//*[normalize-space(text())='Which of these is your priority?']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _select_goal(self, goal_value: str):
        self.log.info(f"🎯 Selecting goal: {goal_value}")
        safe_value = self.escape_xpath_text(goal_value)
        goal_option = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")
        goal_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        goal_option.click()
        expect(goal_option).to_be_visible(timeout=3000)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
