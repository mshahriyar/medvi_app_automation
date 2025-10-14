
from playwright.sync_api import Page, expect
import logging
import allure


class lastThreeMonthMedicationPage:


    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("astThreeMonthMedicationPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify last three month medication heading")
    def verify_last_three_month_medication_heading(self):
        """Verify last three month medication heading."""
        self.log.info(f"💊 Verifying last three month medication heading:")
        verify_last_three_month_medication_heading = self.frame.locator("//span[text() ='Within the last 3 months, have you taken opiate pain medications and/or opiate-based street drugs?']")
        expect(verify_last_three_month_medication_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Last three month medication heading verified successfully")
    
    @allure.step("Select last three month medication option (Yes/No)")
    def select_last_three_month_medication_option(self, option: str, medication_name: str = None):
        """Select Yes/No and handle conditional medication name input if Yes is chosen."""
        clean_option = option.strip().capitalize()
        self.log.info(f"💊 Selecting last three month medication option: {clean_option}")

        # Click Yes or No
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{clean_option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected option: {clean_option}")

        # Conditional field: only appears if 'Yes' is selected
        if clean_option == "Yes":
            self.log.info("🩺 User selected 'Yes' — waiting for medication input field...")
            medication_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")

            try:
                medication_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                if medication_name:
                    medication_input.fill(medication_name)
                    self.log.info(f"✅ Entered medication name: {medication_name}")
                else:   
                    self.log.info(f"✅ No medication name provided, field left blank.")
                    
            except Exception as e:
                self.log.error(f"❌ Medication input field not visible after selecting 'Yes': {e}")
                raise

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
     