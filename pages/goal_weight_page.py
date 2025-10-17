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
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Utilities ---------------------- #
    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath — handles both single and double quotes."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # ---------------------- Actions ---------------------- #
    @allure.step("Verify goal weight page heading displayed")
    def verify_goal_weight_page_heading_displayed(self):
        """Verify the goal weight page heading displayed."""
        self.log.info("🔍 Verifying goal weight page heading displayed...")

        # Safely escaped text for both headings
        safe_text_1 = self.escape_xpath_text("We're in this together.")
        safe_text_2 = self.escape_xpath_text("What is your goal weight?")

        heading_1 = self.frame.locator(f"//*[normalize-space(text())={safe_text_1}]")
        heading_2 = self.frame.locator(f"//*[normalize-space(text())={safe_text_2}]")

        expect(heading_1).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(heading_2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Goal weight page headings verified successfully")

    @allure.step("Enter goal weight")
    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        self.log.info(f"⚖️ Entering goal weight: {goal_weight}")

        goal_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        goal_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        goal_input.fill(goal_weight)

        expect(goal_input).to_have_value(goal_weight, timeout=5000)
        self.log.info("✅ Goal weight entered successfully")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
