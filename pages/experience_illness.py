from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import logging

class ExperienceIllnessPage(BasePage):
    """Handles 'Experience Illness' step interactions in the MEDVi Typeform flow."""
    log = logging.getLogger("ExperienceIllnessPage")
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Dynamic template for illness options
        self.option_template = "//div[normalize-space(text())='{experience_illness}']"

        # Buttons
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # Headings
        self.main_heading = self.frame.locator("h1")
        self.question_heading = self.frame.locator("h2")

        # Common illness options
        self.low_libido = self.frame.locator("text=Low Libido")
        self.hair_loss = self.frame.locator("text=Hair Loss")
        self.skin_issues = self.frame.locator("text=Skin Issues")
        self.cognition = self.frame.locator("text=Cognition")
        self.none_option = self.frame.locator("text=None of these")

        # SVG icons
        self.trending_icon = self.frame.locator("svg[data-src*='trending-down.svg']")
        self.svg_icons = self.frame.locator(
            "svg[data-src*='medical'], svg[data-src*='health'], svg[data-src*='illness']"
        )

        # Header
        self.medvi_logo = self.page.locator("text=MEDVI")
        self.rating_text = self.page.locator("text=Excellent 4.7")
        self.treviews_logo = self.page.locator("img[src*='treviews.png']")

    # -------------------- Actions --------------------

    def select_experience_illness(self, experience_illness_value: str):
        """
        Selects an illness option dynamically based on provided value.
        Example: 'Hair Loss', 'Skin Issues', etc.
        """
        clean_value = experience_illness_value.strip()
        self.log.info(f"Selecting experience illness: '{clean_value}'")

        # Build the locator dynamically
        locator_xpath = self.option_template.format(experience_illness=clean_value)
        option_locator = self.frame.locator(locator_xpath)

        try:
            # Wait and verify visibility
            option_locator.wait_for(state="visible", timeout=10000)
            option_locator.scroll_into_view_if_needed()
            expect(option_locator).to_be_visible(timeout=5000)
            option_locator.click()
            self.log.info(f"Successfully selected: '{clean_value}'")

        except Exception as e:
            self.log.info(f"Failed to select '{clean_value}': {e}")
            # Optional: log all available options for debugging
            available_options = self.frame.locator("//div[contains(@class, 'option')]")
            count = available_options.count()
            self.log.info(f"Found {count} available options:")
            for i in range(min(count, 10)):
                text = available_options.nth(i).text_content()
                self.log.info(f"  - {text}")
            raise

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("Clicked 'Next' button")
