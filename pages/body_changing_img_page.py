from playwright.sync_api import Page, expect
import logging
import allure


class BodyChangingImgPage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("BodyChangingImgPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify body changing img heading and image")
    def verify_body_changing_img_heading(self):
        self.log.info(f"💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='/tatman1.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Image displayed verified successfully")

        self.log.info(f"💊 Verifying weight change last year heading:")
        is_visible = self.frame.locator("h2").is_visible()
        if is_visible:
            print("✅ H2 element is visible on the page")
        else:
            print("❌ H2 element is not visible")


    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")