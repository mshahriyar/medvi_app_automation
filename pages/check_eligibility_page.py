import logging
import allure
from playwright.sync_api import Page, expect

class CheckEligibilityPage:
    """Handles the 'Check Eligibility' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("CheckEligibilityPage")    

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @allure.step("Verify check eligibility page heading displayed")
    def verify_check_eligibility_content_displayed(self):
        """Verify the check eligibility content displayed."""
        self.log.info("🔍 Verifying check eligibility content displayed...")
        content = self.frame.locator("//*[text() ='how can you be reached if necessary?']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Check eligibility content displayed verified successfully")

    @allure.step("Add email")
    def add_email(self, value: str):
        """Add email value."""
        self.log.info(f"🔍 Adding email: {value}")
        email_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        email_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        email_input.fill(value)
        expect(email_input).to_have_value(value)
        self.log.info(f"✅ Added email: {value}")
    
    @allure.step("Add phone")
    def add_phone(self, value: str):
        """Add phone value."""
        self.log.info(f"🔍 Adding phone: {value}")
        phone_input = self.frame.locator("(//*[normalize-space(text())='Phone Number']/ancestor::div//input[@type='tel'])[1]")
        phone_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        phone_input.fill(value)
        self.log.info(f"✅ Added phone: {value}")

    @allure.step("image is displayed")
    def verify_image_displayed(self):
        """Verify the image displayed."""
        self.log.info("🔍 Verifying image displayed...")
        usa_image = self.frame.locator("img[src*='Made-in-USA-Badge.jpg']")
        expect(usa_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        hippa_image = self.frame.locator("img[src*='/HIPAA-Compliant.png']")
        expect(hippa_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Image displayed verified successfully")

    @allure.step("Click 'Next' button on check eligibility page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")