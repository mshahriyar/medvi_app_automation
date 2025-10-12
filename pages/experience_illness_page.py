from playwright.sync_api import Page, expect
import logging


class ExperienceIllnessPage:
    """Handles 'Experience Illness' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("ExperienceIllnessPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Dynamic template for illness options
        self.option_template = "//div[normalize-space(text())='{experience_illness}']"
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def select_experience_illness(self, experience_illness_value: str):
        """Selects an illness option dynamically based on provided value."""
        clean_value = experience_illness_value.strip()
        self.log.info(f"🩺 Selecting experience illness: '{clean_value}'")

        # Build the locator dynamically
        locator_xpath = self.option_template.format(experience_illness=clean_value)
        option_locator = self.frame.locator(locator_xpath)

        try:
            # Wait and verify visibility
            option_locator.wait_for(state="visible", timeout=10000)
            option_locator.scroll_into_view_if_needed()
            expect(option_locator).to_be_visible(timeout=5000)
            option_locator.click()
            self.log.info(f"✅ Successfully selected: '{clean_value}'")

        except Exception as e:
            self.log.error(f"❌ Failed to select '{clean_value}': {e}")
            raise

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
