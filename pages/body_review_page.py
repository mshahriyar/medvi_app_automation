from playwright.sync_api import Page, expect
import logging
import allure


class BodyReviewPage:
    """Handles the 'Body Review' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("BodyReviewPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify Body Review content")
    def verify_body_review_content(self):
        """Verify that the heading and image are visible on the Body Review page."""
        self.log.info("🔍 Verifying Body Review content...")

        heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'Thank you for the metabolic reset - game changer')]"
        )
        image = self.frame.locator("img[src*='/13.png']")

        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Body Review heading and image verified successfully")

    @allure.step("Click 'Next' button on Body Review page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
