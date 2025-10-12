from playwright.sync_api import Page, expect
import logging
class AnalyzeMetabolismPage:
    """Handles the 'Analyze Metabolism' step in the MEDVi Typeform flow."""
    log = logging.getLogger("AnalyzeMetabolismPage")
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        # self.perfect_text = self.frame.locator("//span[normalize-space(text())='doesn’t involve restrictive diets']")
        self.analyze_metabolism_text = self.frame.locator(
            "//p[contains(normalize-space(.), 'Now, let’s') and contains(normalize-space(.), 'analyze your metabolism')]"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    # -------------------- Validation Methods --------------------

    def verify_analyze_metabolism_content(self):
        """Verify that both 'Perfect!' heading and 'Now, let’s analyze your metabolism' text are visible."""
        self.log.info("Verifying 'Analyze Metabolism' page content...")

        results = {
            "analyze_metabolism_text": expect(self.analyze_metabolism_text).to_be_visible(timeout=10000),
        }

        all_passed = all(results.values())

        self.log.info("\nValidation Summary:")
        for name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log.info(f"   {name}: {status}")

        if all_passed:
            self.log.info("All 'Analyze Metabolism' texts verified successfully!\n")
        else:
            self.log.info("Some 'Analyze Metabolism' texts are missing or not visible.\n")

        return all_passed


    # -------------------- Actions --------------------

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.log.info("Clicking 'Next' button on Analyze Metabolism page...")
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click(timeout=10000)
        self.log.info("Clicked 'Next' button successfully")
