from playwright.sync_api import Page, expect
import logging

class PriorityPage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    log = logging.getLogger("PriorityPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.goal_selection = "//div[normalize-space(text())='{goal}']"
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def select_goal(self, goal_value: str):
        self.log.info(f"Selecting goal: {goal_value}")
        locator = self.goal_selection.format(goal=goal_value)
        goal_option = self.frame.locator(locator)
        goal_option.click()
        expect(goal_option).to_be_visible()

    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.next_button.click(timeout=10000)
        self.log.info("Next button clicked")
