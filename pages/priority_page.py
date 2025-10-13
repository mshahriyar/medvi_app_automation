from playwright.sync_api import Page, expect
import logging
import allure


class PriorityPage:
    """Handles 'Priority' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("PriorityPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale reference."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Select user goal priority")
    def select_goal(self, goal_value: str):
        """Selects a goal (Lose Weight / Gain Muscle / Maintain)."""
        self.log.info(f"🎯 Selecting goal: {goal_value}")

        goal_option = self.frame.locator(f"//div[normalize-space(text())='{goal_value}']")
        goal_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        goal_option.click()

        expect(goal_option).to_be_visible(timeout=3000)
        self.log.info(f"✅ Selected goal: {goal_value}")

    @allure.step("Click 'Next' button on Priority page")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
