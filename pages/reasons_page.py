from playwright.sync_api import Page, expect
import logging


class ReasonsPage:
    """Handles reasons selection in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("ReasonsPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")
        self.reasons_heading = self.frame.locator("//span[contains(text(), 'Improving your life requires ')]")

    def verify_reasons_heading_visible(self):
        """Verify the reasons heading is visible."""
        self.log.info("🔍 Verifying reasons heading...")
        expect(self.reasons_heading).to_be_visible(timeout=10000)
        self.log.info("✅ Reasons heading visible")

    def select_reason(self, reason: str):
        """Select a reason for weight loss."""
        self.log.info(f"🎯 Selecting reason: {reason}")
        reason_locator = self.frame.locator(f"//div[normalize-space(text())='{reason}']")
        reason_locator.wait_for(state="visible", timeout=10000)
        reason_locator.click()
        self.log.info(f"✅ Reason selected: {reason}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
