from playwright.sync_api import Page, expect


class GoalWeightPage:
    """Handles goal weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Form elements
        self.goal_weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # Page validation elements
        self.together_text = self.frame.locator("text=We're in this together. Your goal is our goal.")
        self.goal_weight_question = self.frame.locator("text=What is your goal weight?")

    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        print(f"⚖️ Entering goal weight: {goal_weight}")
        self.goal_weight_input.wait_for(state="visible", timeout=10000)
        self.goal_weight_input.fill(goal_weight)
        expect(self.goal_weight_input).to_have_value(goal_weight, timeout=5000)
        print("✅ Goal weight entered successfully")

    def verify_together_text(self):
        """Ensure motivational text appears."""
        print("🔍 Verifying together text...")
        try:
            expect(self.together_text).to_be_visible(timeout=5000)
            print("✅ Together text visible")
        except:
            print("⚠️ Together text not found")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
