from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import logging


class GoalWeightPage(BasePage):
    """Handles goal weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("GoalWeightPage")

    def __init__(self, page: Page):
        super().__init__(page)
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Form elements
        self.goal_weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # Page validation elements
        self.together_text = self.frame.locator("text=We're in this together. Your goal is our goal.")
        self.goal_weight_question = self.frame.locator("text=What is your goal weight?")

        # Header elements (on the main page)
        self.medvi_logo = self.page.locator("text=MEDVi")
        self.rating_text = self.page.locator("text=Excellent 4.7")
        self.treviews_logo = self.page.locator("img[src*='treviews.png']")

    # -------------------- Form Interactions --------------------

    def add_goal_weight(self, goal_weight: str):
        """Enter goal weight (lbs) into the input field."""
        self.log.info(f"⚖️ Entering goal weight: {goal_weight}")
        self.goal_weight_input.wait_for(state="visible", timeout=10000)
        self.goal_weight_input.fill(goal_weight)
        expect(self.goal_weight_input).to_have_value(goal_weight, timeout=5000)
        self.log.info("✅ Goal weight entered successfully")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click(timeout=10000)
        self.log.info("➡️ Clicked 'Next' button")

    # -------------------- Validations --------------------

    def verify_page_loaded(self):
        """Basic validation that key text and input are visible."""
        self.log.info("🔍 Verifying goal weight page loaded...")
        expect(self.goal_weight_question).to_be_visible(timeout=10000)
        expect(self.goal_weight_input).to_be_visible(timeout=10000)
        self.log.info("✅ Goal weight question and input visible")

    def verify_header_elements(self):
        """Verify MEDVi and TReviews logos are visible."""
        self.log.info("🔍 Verifying header elements...")
        for name, locator in [
            ("MEDVi logo", self.medvi_logo),
            ("Rating text", self.rating_text),
            ("TReviews logo", self.treviews_logo),
        ]:
            try:
                expect(locator).to_be_visible(timeout=5000)
                self.log.info(f"✅ {name} visible")
            except:
                self.log.warning(f"⚠️ {name} not found")

    def verify_together_text(self):
        """Ensure motivational text appears."""
        self.log.info("🔍 Verifying together text...")
        try:
            expect(self.together_text).to_be_visible(timeout=5000)
            self.log.info("✅ Together text visible")
        except:
            self.log.warning("⚠️ Together text not found")

    def validate_page(self):
        """Run all key verifications together."""
        self.verify_page_loaded()
        self.verify_together_text()
        self.verify_header_elements()
        self.log.info("✅ Goal weight page validation complete")
