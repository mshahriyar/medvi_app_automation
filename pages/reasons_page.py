from playwright.sync_api import Page, expect
import logging
import allure


class ReasonsPage:
    """Handles reasons selection in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("ReasonsPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify reasons heading is visible")
    def verify_reasons_heading_visible(self):
        """Verify the reasons heading is visible."""
        self.log.info("🔍 Verifying reasons heading...")

        heading = self.frame.locator("//span[contains(text(), 'Improving your life requires ')]")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Reasons heading verified successfully")

    @allure.step("Select reason for weight loss")
    def select_reason(self, reason: str):
        """Select a reason for weight loss."""
        self.log.info(f"🎯 Selecting reason: {reason}")

        reason_locator = self.frame.locator(f"//div[normalize-space(text())='{reason}']")
        reason_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        reason_locator.click()

        self.log.info(f"✅ Reason selected: {reason}")

    @allure.step("Click 'Next' button on Reasons page")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()

        self.log.info("➡️ Clicked 'Next' button")
