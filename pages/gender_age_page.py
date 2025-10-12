from playwright.sync_api import Page, expect
import logging


class GenderAndAgePage:
    """Handles gender and age selection interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GenderAndAgePage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Form elements
        self.gender_option = "//div[normalize-space(text())='{gender}']"
        self.age_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def select_gender(self, gender: str):
        """Select Male or Female dynamically."""
        self.log.info(f"👤 Selecting gender: {gender}")
        gender_locator = self.frame.locator(self.gender_option.format(gender=gender))
        gender_locator.wait_for(state="visible", timeout=10000)
        gender_locator.click()
        self.log.info(f"✅ Selected gender: {gender}")

    def select_age(self, age: str):
        """Select the user's age range from dropdown."""
        self.log.info(f"🎂 Selecting age range: {age}")
        self.age_dropdown.wait_for(state="visible", timeout=10000)
        self.age_dropdown.click()
        self.page.wait_for_timeout(500)

        # Try multiple matching strategies for reliability
        possible_age_options = [
            f"//div[contains(text(), '{age}')]",
            f"//div[contains(text(), '{age.split('–')[0]}')]" if '–' in age else f"//div[contains(text(), '{age.split('-')[0]}')]",
        ]

        age_option = None
        for selector in possible_age_options:
            locator = self.frame.locator(f"(//div[@data-cy='dropdown-component'])[1]{selector}")
            if locator.count() > 0:
                age_option = locator.first
                break

        if age_option:
            age_option.click()
            self.log.info(f"✅ Selected age range: {age}")
        else:
            self.log.error(f"❌ Could not find age option: {age}")
            raise Exception(f"Age option '{age}' not found in dropdown")

    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
