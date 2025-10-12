from playwright.sync_api import Page, expect
import logging
class BodyReviewPage:

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("BodyReviewPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.body_review_heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'Thank you for the metabolic reset - game changer')]"
        )
        self.body_review_image = self.frame.locator("img[src*='/13.png']")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    # -------------------- Validations --------------------

    def verify_body_review_content(self):
        """Verify that the heading and image are visible on the Body Review page."""
        self.log.info("Verifying 'Body Review' page content...")

        validation_results = {
            "body_review_heading": expect(self.body_review_heading).to_be_visible(timeout=10000),
            "body_review_image": expect(self.body_review_image).to_be_visible(timeout=10000),
        }

        all_passed = all(validation_results.values())

        self.log.info("\nBody Review Page Validation Summary:")
        for name, result in validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log.info(f"   {name}: {status}")

        if all_passed:
            self.log.info("All Body Review elements verified successfully!\n")
        else:
            self.log.info("Some elements are missing or not visible.\n")

        return all_passed

    # -------------------- Actions --------------------

    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        self.log.info("Clicking 'Next' button on Body Review page...")
        try:
            self.next_button.wait_for(state="visible", timeout=10000)
            self.next_button.click(timeout=10000)
            self.log.info("Clicked 'Next' button successfully")
        except Exception as e:
            self.log.info(f"Failed to click 'Next' button: {e}")
            raise
