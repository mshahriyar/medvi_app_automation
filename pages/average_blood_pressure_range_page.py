from playwright.sync_api import Page, expect
import logging
import allure


class AverageBloodPressureRangePage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("AverageBloodPressureRangePage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify average blood pressure range heading and image")
    def verify_average_blood_pressure_range_heading(self):
        self.log.info(f"💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='3d858dffa6d6_1.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Image displayed verified successfully")

        self.log.info(f"💊 Verifying average blood pressure range heading:")
        is_visible = self.frame.locator("//span[text() ='What is your average blood pressure range?']").is_visible()
        if is_visible:
            print("✅ Average blood pressure range heading is visible on the page")
        else:
            print("❌ Average blood pressure range heading is not visible")

    @allure.step("Select average blood pressure range option")
    def select_average_blood_pressure_range_option(self):
        self.log.info(f"💊 Selecting average blood pressure range option:")
        # Click Yes or No
        option_locator = self.frame.locator("//div[normalize-space(text())='<120/80 (Normal)']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected option: <120/80 (Normal)")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")