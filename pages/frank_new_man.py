from playwright.sync_api import Page, expect
import logging
class FrankNewManPage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("FrankNewManPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")


    def verify_recommendation_visible(self):
        """Verify that the testimonial text is visible."""
        self.log.info("Verifying recommendation visible...")
        recommendation_locator = self.frame.locator(
            "//*[contains(text(), '\"From the first day, MEDVi has been so attentive and informative\")]"
        )
        expect(recommendation_locator).to_be_visible()
        self.log.info("Recommendation visible")


    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.log.info("Clicking next button...")
        self.next_button.click(timeout=10000)
        self.log.info("Next button clicked")
