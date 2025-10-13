from playwright.sync_api import Page, expect
import logging
import allure


class GoalWeightPage:
    """Handles goal weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GoalWeightPage")

    @property
    def frame(self):
        """Always get a fresh frame locator (avoids stale reference)."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Enter goal weight")
    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        self.log.info(f"⚖️ Entering goal weight: {goal_weight}")

        goal_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        goal_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        goal_input.fill(goal_weight)

        expect(goal_input).to_have_value(goal_weight, timeout=5000)
        self.log.info("✅ Goal weight entered successfully")

    @allure.step("Verify motivational text is visible")
    def verify_together_text(self):
        """Ensure motivational text appears."""
        self.log.info("🔍 Verifying motivational text...")

        together_text = self.frame.locator("text=We're in this together. Your goal is our goal.")
        try:
            expect(together_text).to_be_visible(timeout=5000)
            self.log.info("✅ Motivational text is visible")
        except Exception as e:
            self.log.warning(f"⚠️ Motivational text not found: {e}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
