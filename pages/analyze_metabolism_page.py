from playwright.sync_api import Page, expect
import logging
import allure


class AnalyzeMetabolismPage:
    """Handles the 'Analyze Metabolism' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("AnalyzeMetabolismPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify 'Analyze Metabolism' content is visible")
    def verify_analyze_metabolism_content(self):
        """Verify that the 'analyze metabolism' text is visible."""
        self.log.info("🔍 Verifying analyze metabolism content...")

        analyze_text = self.frame.locator(
            "//p[contains(normalize-space(.), 'analyze your metabolism')]"
        )
        expect(analyze_text).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Analyze metabolism content verified successfully")

    @allure.step("Click 'Next' button on Analyze Metabolism page")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()

        self.log.info("➡️ Clicked 'Next' button")
