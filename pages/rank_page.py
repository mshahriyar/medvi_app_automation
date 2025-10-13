from playwright.sync_api import Page, expect
import logging
import allure


class RankPage:
    """Handles the Rank verification step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("RankPage")

    @property
    def frame(self):
        """Return a fresh frame locator to avoid stale reference."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify Forbes rank image is visible")
    def verify_rank(self):
        """Verify that the Forbes #1 rank image is displayed."""
        self.log.info("🏆 Verifying Forbes rank image visibility...")
        rank_image = self.frame.locator("img[src*='forbes-number-1.png']")
        rank_image.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        expect(rank_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Rank image verified successfully")

    @allure.step("Click 'Next' button on Rank page")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
