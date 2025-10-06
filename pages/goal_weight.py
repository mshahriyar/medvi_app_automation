from playwright.sync_api import Page, expect

class GoalWeightPage:
    

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.goal_weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")


    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        self.goal_weight_input.fill(goal_weight)
        self.page.wait_for_timeout(2000)
        expect(self.goal_weight_input).to_have_value(goal_weight, timeout=5000)

    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.next_button.click(timeout=10000)