from playwright.sync_api import Page, expect
import logging
import allure


class FrankNewManPage:
    """Handles testimonial verification in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("FrankNewManPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify testimonial text is visible")
    def verify_recommendation_visible(self):
        """Verify that the testimonial text is visible inside the iframe."""
        self.log.info("🔍 Verifying testimonial visibility...")

    # Combine both locators (h2 + p) into one
        recommendation_locator = self.frame.locator(
            "//h2[contains(@class, 'ql-align-center')] | //p[contains(@class, 'ql-align-center')]"
        )

        # Wait for visibility
        expect(recommendation_locator.first).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Testimonial text verified successfully")

    @allure.step("Click 'Next' button on testimonial page")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
