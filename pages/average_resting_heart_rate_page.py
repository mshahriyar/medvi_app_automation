from playwright.sync_api import Page, expect
import logging
import allure


class AverageRestingHeartRatePage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("AverageRestingHeartRatePage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify average resting heart rate heading and image")       
    def verify_average_resting_heart_rate_heading(self):
        self.log.info(f"💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='9c488a250fc7_0.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Image displayed verified successfully")

        self.log.info(f"💊 Verifying average resting heart rate heading:")
        is_visible = self.frame.locator("//span[text() ='How about your average resting heart rate?']").is_visible()
        if is_visible:
            print("✅ Average resting heart rate heading is visible on the page")
        else:
            print("❌ Average resting heart rate heading is not visible")

    @allure.step("Select average resting heart rate option")
    def select_average_resting_heart_rate_option(self):
        self.log.info(f"💊 Selecting average resting heart rate option:")
        # Click Yes or No
        option_locator = self.frame.locator("//div[normalize-space(text())='60-100 beats per minute (Normal)']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected option: 60-100 beats per minute (Normal)")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")