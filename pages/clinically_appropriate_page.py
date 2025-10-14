from playwright.sync_api import Page, expect
import logging
import allure


class ClinicallyAppropriatePage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("ClinicallyAppropriatePage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify clinically appropriate heading")
    def verify_clinically_appropriate_heading(self):
        self.log.info(f"💊 Verifying clinically appropriate heading:")
        verify_surgery_weight_loss_heading = self.frame.locator("//span[normalize-space(text())='If clinically appropriate, are you willing to:']")
        expect(verify_surgery_weight_loss_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Clinically appropriate heading verified successfully")

    @allure.step("Select clinically appropriate option")
    def select_clinically_appropriate_option(self, option: str):
        self.log.info(f"💊 Selecting clinically appropriate option: {option}")
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected clinically appropriate option: {option}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")