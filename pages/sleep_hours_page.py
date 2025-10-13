from playwright.sync_api import Page, expect
import logging
import allure


class SleepHoursPage:
    """Handles the 'Sleep Hours' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("SleepHoursPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify sleep hours question and image are visible")
    def verify_sleep_heading_and_image(self):
        """Verify that the question text and image are visible."""
        self.log.info("🔍 Verifying sleep heading and image...")

        sleep_heading = self.frame.locator(
            "//*[normalize-space(text())='How many hours of sleep do you usually get each night?']"
        )
        sleep_image = self.frame.locator(
            "img[src*='id-1tAZd12DZCus/widgetid-k1Xy/hHZFcPL7X59pJZtoxUx5JW/gallaghergallagher_Romantic_lifestyle_photography_style_warm__cdfcbe67-e11e-45d2-8ef5-2f0a6d85ca4c_3.png']"
        )

        expect(sleep_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(sleep_image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Sleep heading and image verified")

    @allure.step("Select sleep hours option")
    def select_sleep_hours(self, sleep_hours: str):
        """Select a sleep hours option dynamically."""
        self.log.info(f"😴 Selecting sleep hours option: {sleep_hours}")

        locator_str = f"//div[normalize-space(text())='{sleep_hours}']"
        sleep_option = self.frame.locator(locator_str)

        sleep_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        sleep_option.scroll_into_view_if_needed()
        expect(sleep_option).to_be_visible(timeout=5000)
        sleep_option.click()

        self.log.info(f"✅ Selected sleep hours option: {sleep_hours}")

    @allure.step("Click 'Next' button on Sleep Hours page")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()

        self.log.info("➡️ Clicked 'Next' button")
