
from playwright.sync_api import Page, expect
import logging
import allure


class GLP1MedicinePage:
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
    
    def escape_xpath_text(self, text: str) -> str:
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
    
    @allure.step("Enter name dose frequency")
    def enter_name_dose_frequency(self):
        """Enter name dose frequency."""
        self.log.info(f"💊 Entering name dose frequency:")
        verify_name_dose_heading = self.frame.locator("//span[text() ='Please list the name, dose, and frequency of your GLP-1 medication.']")
        expect(verify_name_dose_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        name_dose_frequency = self.frame.locator("//*[@id='widget-qbjC']//textarea")
        name_dose_frequency.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        name_dose_frequency.fill("Panadol 100mg")
        self.log.info(f"✅ Name dose frequency entered successfully")

    @allure.step("Enter last dose days")
    def enter_last_dose_days(self, last_dose_days: str):    
        """Selects the option for last dose days dynamically."""
        self.log.info(f"💉 Selecting last dose days: '{last_dose_days}'")
        verify_last_dose_heading = self.frame.locator("//span[text() ='When was your last dose of medication?']")
        expect(verify_last_dose_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        option_locator = self.frame.locator(f"//div[text()='{last_dose_days}']")
        option_locator.wait_for(state="visible", timeout=10000)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()

        self.log.info(f"✅ Selected last dose days: '{last_dose_days}'")

    @allure.step("Enter starting weight")
    def enter_starting_weight(self):
        """Enter starting weight."""
        self.log.info(f"💊 Entering starting weight:")
        verify_starting_weight_heading = self.frame.locator("//span[text() ='What was your starting weight in pounds?']")
        expect(verify_starting_weight_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        starting_weight = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        starting_weight.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        starting_weight.fill("90")
        self.log.info(f"✅ Starting weight entered successfully")

    @allure.step("Upload GLP-1 medication photo")
    def upload_glp1_photo(self, file_path: str):
        """Uploads a GLP-1 medication photo file."""
        verify_upload_glp1_photo_heading = self.frame.locator("//h3[text() ='Please take or upload a photo of your GLP-1 medication']")
        verify_upload_glp1_photo_heading.scroll_into_view_if_needed()
        expect(verify_upload_glp1_photo_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"📸 Uploading medication photo: {file_path}")
        upload_input = self.frame.locator("(//input[@type='file'])[1]")
        upload_input.set_input_files(file_path)
        expect(upload_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Photo uploaded successfully")

    @allure.step("Do you agree to move forward with his program")
    def agree_to_move_forward(self):
        """Agree to move forward with the program."""
        self.log.info("💊 Agreeing to move forward with the program.")
        verify_agree_to_move_forward_heading = self.frame.locator("//span[text() ='Do you agree to only obtain weight loss medication through this program moving forward?']")
        verify_agree_to_move_forward_heading.scroll_into_view_if_needed()
        expect(verify_agree_to_move_forward_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        agree_to_move_forward = self.frame.locator("//div[normalize-space(text())='Yes']")
        agree_to_move_forward.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        agree_to_move_forward.click()
        self.log.info("✅ Agreed to move forward with the program.")


    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click(force=True)
        self.log.info("➡️ Clicked 'Next' button")
        self.page.wait_for_timeout(1000)