import logging
import allure
from playwright.sync_api import Page, expect

class SubmissionFormPage:
    """Handles the 'Submission Form' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("SubmissionFormPage")
    
    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @allure.step("Verify submission form page heading displayed")
    def verify_submission_form_page_heading_displayed(self):
        """Verify the submission form page heading displayed."""
        self.log.info("🔍 Verifying submission form page heading displayed...")
        heading = self.frame.locator("//h1[text()= 'Please review your submission.']")
        content = self.frame.locator("//p[text()= 'You have indicated a health condition which prevents you from being prescribed.']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Submission form page heading and content displayed verified successfully")

    @allure.step("Verify Edit info is working")
    def verify_edit_info_is_working(self):
        """Verify the edit info is working."""
        self.log.info("🔍 Verifying edit info is working...")
        edit_info_button = self.frame.locator("(//*[text() = 'Edit'])[28]")
        expect(edit_info_button).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        edit_info_button.click()
        self.log.info("✅ Edit info is working verified successfully")

    @allure.step("Click 'check eligibility' button on submission form page")
    def hit_check_eligibility_button(self):
        """Click the 'check eligibility' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'check eligibility' button")

    @allure.step("Click 'Submit' button on submission form page")
    def hit_submit_button(self):
        """Click the 'Submit' button to continue."""
        submit_button = self.frame.locator("//*[text()= 'Submit']")
        submit_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        submit_button.click()
        self.log.info("➡️ Clicked 'Submit' button")