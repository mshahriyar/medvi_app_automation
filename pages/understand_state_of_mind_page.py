import logging
import allure
from playwright.sync_api import Page, expect


class UnderstandStateOfMindPage:
    """Handles the 'Understand State of Mind' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("UnderstandStateOfMindPage")      
    
    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath — handles both single and double quotes."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    
    @allure.step("Verify understand state of mind heading")
    def verify_understand_state_of_mind_heading(self, goal_weight: str):
        """Verify the understand state of mind heading."""
        self.log.info("🔍 Verifying understand state of mind heading...")
        heading_1 = self.frame.locator("//h1")
        heading_1.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ H1 element is visible on the page")
        heading_1_text = heading_1.text_content()
        self.log.info(f"✅ H1 element text content: {heading_1_text}")
        heading_2 = self.frame.locator(f"//span[text()='How motivated are you to reach {goal_weight}lbs?']")
        expect(heading_2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Understand state of mind heading verified successfully")

    @allure.step("Select understand state of mind option")
    def select_understand_state_of_mind_option(self, option: str):
        """Select the understand state of mind option."""
        self.log.info(f"💊 Selecting understand state of mind option: {option}")
        xpath_text = self.escape_xpath_text(option)
        option_locator = self.frame.locator(f"xpath=//div[normalize-space(text())={xpath_text}]")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected understand state of mind option: {option}")

    @allure.step("Click 'Next' button on understand state of mind page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")