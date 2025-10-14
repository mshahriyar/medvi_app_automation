from playwright.sync_api import Page, expect
import logging
import allure

class WeightLossProgramPage:
    """Handles the 'Surgery Weight Loss' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("WeightLossProgramPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify weight loss program heading")
    def verify_weight_loss_program_heading(self):
        """Verify last three month medication heading."""
        self.log.info(f"💊 Verifying weight loss program heading:")
        verify_weight_loss_program_heading = self.frame.locator("//h1[text()='How about weight loss programs?']")
        expect(verify_weight_loss_program_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Weight loss program heading verified successfully")
    
    @allure.step("Select weight loss program option (Yes/No)")
    def select_weight_loss_program_option(self, option: str, weight_loss_program_name: str = None):
        """Select Yes/No and handle conditional medication name input if Yes is chosen."""
        clean_option = option.strip().capitalize()
        self.log.info(f"💊 Selecting weight loss program option: {clean_option}")

        # Click Yes or No
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{clean_option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected option: {clean_option}")

        # Conditional field: only appears if 'Yes' is selected
        if clean_option == "Yes":
            self.log.info("🩺 User selected 'Yes' — waiting for weight loss program input field...")
            label_text_locator =self.frame.locator("//span[text()='Please provide brief details.']")
            expect(label_text_locator).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
            weight_loss_program_input = self.frame.locator("//*[@data-cy='long-answer-component']//textarea")

            try:
                weight_loss_program_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                if weight_loss_program_name:
                    weight_loss_program_input.fill(weight_loss_program_name)
                    self.log.info(f"✅ Entered weight loss program name: {weight_loss_program_name}")
                else:   
                    self.log.info(f"✅ No weight loss program name provided, field left blank.")
                    
            except Exception as e:
                self.log.error(f"❌ Weight loss program input field not visible after selecting 'Yes': {e}")
                raise

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
     