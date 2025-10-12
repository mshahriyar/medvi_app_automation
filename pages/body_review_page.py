from playwright.sync_api import Page, expect


class BodyReviewPage:
    """Handles the 'Body Review' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        self.body_review_heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'Thank you for the metabolic reset - game changer')]"
        )
        self.body_review_image = self.frame.locator("img[src*='/13.png']")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_body_review_content(self):
        """Verify that the heading and image are visible on the Body Review page."""
        print("🔍 Verifying body review content...")
        expect(self.body_review_heading).to_be_visible(timeout=10000)
        expect(self.body_review_image).to_be_visible(timeout=10000)
        print("✅ Body review content verified")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
