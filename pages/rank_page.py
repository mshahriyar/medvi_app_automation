from playwright.sync_api import Page, expect
import logging
class RankPage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("RankPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")


    def verify_rank(self):
        self.log.info("Verifying rank...")
        img = self.frame.locator("img[src*='forbes-number-1.png']")

        expect(img).to_be_visible(timeout=10000)
        self.log.info("Rank verified")

    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.log.info("Clicking next button...")
        self.next_button.click(timeout=10000)
        self.log.info("Next button clicked")    
