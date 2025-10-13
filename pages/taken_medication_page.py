# These are three options i have:

# option1: Yes, I've taken GLP-1 medication
# option2: Yes, I've taken a different medication for weight loss
# option3: No

# h2: Have you taken medication for weight loss within the past 4 weeks?
    
from playwright.sync_api import Page, expect
import logging
import allure


class TakenMedicationPage:
    """Handles 'Taken Medication' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("TakenMedicationPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    

    @allure.step("Select taken medication option")
    def select_taken_medication(self, taken_medication_value: str):
        """Select an taken medication option dynamically based on provided value."""
        clean_value = taken_medication_value.strip()
        self.log.info(f"💊 Selecting taken medication: '{clean_value}'")

        option_locator = self.frame.locator(f"xpath=//div[normalize-space(text())='{clean_value}']")

        try:
            option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            option_locator.scroll_into_view_if_needed()
            expect(option_locator).to_be_visible(timeout=5000)
            self.page.pause()
            option_locator.click()
            radio = self.frame.locator(f"xpath=//div[normalize-space(text())='{clean_value}']/../../preceding-sibling::span")
            border_color = radio.evaluate("el => getComputedStyle(el).borderColor")
            expect(border_color).to_have_css("border-color", "rgb(198, 166, 115)")
            #assert border_color == "rgb(198, 166, 115)"
            
            self.log.info(f"✅ Successfully selected: '{clean_value}'")
        except Exception as e:
            msg = f"❌ Failed to select '{clean_value}': {e}"
            self.log.error(msg)
            raise RuntimeError(msg)

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")


