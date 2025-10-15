import allure
from playwright.sync_api import Page, expect
import logging

class YourMedicalReviewPage:
    """Handles the 'Your Medical Review' step in the MEDVi Typeform flow."""
    
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("YourMedicalReviewPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    @allure.step("Verify your medical review heading displayed")
    def verify_your_medical_review_heading_displayed(self):
        """Verify the your medical review heading displayed."""
        self.log.info("🔍 Verifying your medical review heading displayed...")
        heading = self.frame.locator("//h1[text()= 'Your Medical Review']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Your medical review heading displayed verified successfully")

    @allure.step("Verify your medical review content displayed")
    def verify_your_medical_review_content_displayed(self):
        """Verify the your medical review content displayed."""
        self.log.info("🔍 Verifying your medical review content displayed...")
        BMI_content = self.frame.locator("//*[text()= 'BMI']")
        current_weight_content = self.frame.locator("//*[text()= 'Current Weight']")
        goal_weight_content = self.frame.locator("//*[text()= 'Goal Weight']")
        safe_text = self.escape_xpath_text("Let's proceed to check your eligibility.")  
        check_eligible_content = self.frame.locator(f"//*[text()= {safe_text}]")
        first_name_label = self.frame.locator("//*[text()= 'First Name']")
        last_name_label = self.frame.locator("//*[text()= 'Last Name']")
        date_of_birth_label = self.frame.locator("//*[text()= 'What state will your medication be shipped to?']")
        expect(BMI_content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(current_weight_content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(goal_weight_content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(check_eligible_content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Your medical review content displayed verified successfully")

    @allure.step("add first name")
    def add_first_name(self, value: str):
        """Add first name value."""
        self.log.info(f"🔍 Adding first name: {value}")
        first_name_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        first_name_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        first_name_input.fill(value)
        expect(first_name_input).to_have_value(value)
        self.log.info(f"✅ Added first name: {value}")

    @allure.step("add last name")    
    def add_last_name(self, value: str):
        """Add last name value."""
        self.log.info(f"🔍 Adding last name: {value}")
        last_name_input = self.frame.locator("(//input[@data-cy='input-component'])[2]")
        last_name_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        last_name_input.fill(value)
        expect(last_name_input).to_have_value(value)
        self.log.info(f"✅ Added last name: {value}")

    @allure.step("Select shipping state")
    def select_shipping_state(self, value: str):
        """Select shipping state value."""
        self.log.info(f"🔍 Selecting shipping state: {value}")
        shipping_state_input = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        shipping_state_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        shipping_state_input.click()
        shipping_state_input.fill(value)
        self.page.keyboard.press("Enter")
        self.log.info(f"✅ Selected shipping state: {value}")

    @allure.step("Click 'Next' button on your medical review page")
    def hit_next_button(self):
        """Click next button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()