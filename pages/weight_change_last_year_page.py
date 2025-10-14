from playwright.sync_api import Page, expect
import logging
import allure


class WeightChangeLastYearPage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("WeightChangeLastYearPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
    
    @allure.step("Verify weight change last year heading and image")
    def verify_weight_change_last_year_heading(self):
        self.log.info(f"💊 Verifying image displayed:")
        verify_image_displayed = self.frame.locator("img[src*='88512fd1dfc0_1.png']")
        expect(verify_image_displayed).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Image displayed verified successfully")

        self.log.info(f"💊 Verifying weight change last year heading:")
        verify_weight_change_last_year_heading = self.frame.locator("//span[normalize-space(text())='Has your weight changed in the last year?']")
        expect(verify_weight_change_last_year_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info(f"✅ Weight change last year heading verified successfully")

    @allure.step("Select weight change last year option")
    def select_weight_change_last_year_option(self, option: str):
        self.log.info(f"💊 Selecting weight change last year option: {option}")
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        self.log.info(f"✅ Selected weight change last year option: {option}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")