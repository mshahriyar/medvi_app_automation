
from playwright.sync_api import Page, expect
import logging
import allure


class lastThreeMonthMedicationPage:
    """Handles GLP-1 medicine step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GLP1MedicinePage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    # def escape_xpath_text(self, text: str) -> str:
    #     if "'" not in text:
    #         return f"'{text}'"
    #     if '"' not in text:
    #         return f'"{text}"'
    #     parts = text.split("'")
    #     return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
    
    @allure.step("Verify last three month medication heading")
    def verify_last_three_month_medication_heading(self):
        """Verify last three month medication heading."""
        self.log.info(f"💊 Verifying last three month medication heading:")
        verify_last_three_month_medication_heading = self.frame.locator("//span[text() ='Within the last 3 months, have you taken opiate pain medications and/or opiate-based street drugs?']")
        expect(verify_last_three_month_medication_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Last three month medication heading verified successfully")
    
    @allure.step("Tell me ast three month medication you took or not")
    def select_last_three_month_medication_option(self, last_three_month_medication_option: str):

        self.log.info(f"💊 Selecting last three month medication option: {last_three_month_medication_option}")
        last_three_month_medication_option = self.frame.locator(f"//div[text()='{last_three_month_medication_option}']")
        last_three_month_medication_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        expect(last_three_month_medication_option).to_be_visible(timeout=5000)
        last_three_month_medication_option.scroll_into_view_if_needed()
        last_three_month_medication_option.click()
        self.log.info(f"✅ Last three month medication option selected successfully")
    
    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
     