from playwright.sync_api import Page, expect
import logging
class ReasonsPage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("ReasonsPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")
        self.reasons_heading = self.frame.locator(
        "//span[contains(text(), 'Improving your life requires ')]")


    def verify_reasons_heading_visible(self):
        self.log.info("Verifying Reasons heading text...")
        expect(self.reasons_heading).to_be_visible(timeout=10000)
        self.log.info("Reasons heading text is visible")

    def select_reason(self, reason: str):
        """Select a reason for weight loss."""
        self.log.info(f"Selecting reason: {reason}")
        self.frame.locator(f"//div[normalize-space(text())='{reason}']").click()
        self.log.info(f"Reason selected: {reason}")
        
    def hit_next_button(self):
        """Click the 'Next' button."""
        self.log.info("Clicking next button...")
        self.next_button.click()
        self.log.info("Next button clicked")
