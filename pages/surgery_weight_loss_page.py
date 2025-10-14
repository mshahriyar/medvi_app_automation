from playwright.sync_api import Page, expect
import logging
import allure

class SurgeryWeightLossPage:
    """Handles the 'Surgery Weight Loss' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("SurgeryWeightLossPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify surgery weight loss heading")
    def verify_surgery_weight_loss_heading(self):
        """Verify last three month medication heading."""
        self.log.info(f"💊 Verifying surgery weight loss heading:")
        verify_surgery_weight_loss_heading = self.frame.locator("//span[text()='Have you had prior weight loss surgeries?']")
        expect(verify_surgery_weight_loss_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Surgery weight loss heading verified successfully")
    
    @allure.step("Select surgery weight loss option (Yes/No)")
    def select_surgery_weight_loss_option(self, option: str, surgery_weight_loss_name: str = None):
        """Select Yes/No and handle conditional medication name input if Yes is chosen."""
        clean_option = option.strip().capitalize()
        self.log.info(f"💊 Selecting surgery weight loss option: {clean_option}")

        # Click Yes or No
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{clean_option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected option: {clean_option}")

        # Conditional field: only appears if 'Yes' is selected
        if clean_option == "Yes":
            self.log.info("🩺 User selected 'Yes' — waiting for surgery weight loss input field...")
            label_text_locator =self.frame.locator("//span[text()='Please include date range and type of surgery.']")
            expect(label_text_locator).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
            surgery_weight_loss_input = self.frame.locator("//*[@data-cy='long-answer-component']//textarea")

            try:
                surgery_weight_loss_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                if surgery_weight_loss_name:
                    surgery_weight_loss_input.fill(surgery_weight_loss_name)
                    self.log.info(f"✅ Entered surgery weight loss name: {surgery_weight_loss_name}")
                else:   
                    self.log.info(f"✅ No surgery weight loss name provided, field left blank.")
                    
            except Exception as e:
                self.log.error(f"❌ Surgery weight loss input field not visible after selecting 'Yes': {e}")
                raise

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
     