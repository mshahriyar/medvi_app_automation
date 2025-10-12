from playwright.sync_api import Page, expect


class AnalyzeMetabolismPage:
    """Handles the 'Analyze Metabolism' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.analyze_metabolism_text = self.frame.locator(
            "//p[contains(normalize-space(.), 'analyze your metabolism')]"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_analyze_metabolism_content(self):
        """Verify that the analyze metabolism text is visible."""
        print("🔍 Verifying analyze metabolism content...")
        expect(self.analyze_metabolism_text).to_be_visible(timeout=10000)
        print("✅ Analyze metabolism content verified")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
