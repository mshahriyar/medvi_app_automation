from playwright.sync_api import Page, expect
import logging
import allure


class SleepCheckPage:
    """Handles the 'Sleep Check' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("SleepCheckPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Helpers ---------------------- #

    def _escape_xpath_text(self, text: str) -> tuple[str, str]:
        """Return the correct quote type for XPath text safely."""
        quote = '"' if "'" in text else "'"
        return quote, text

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify sleep routine heading is visible")
    def verify_sleep_routine_heading_visible(self):
        """Verify that the sleep routine heading is visible."""
        self.log.info("🔍 Verifying sleep routine heading...")

        heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'How you sleep tells us a lot about your')]"
        )
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Sleep routine heading visible")

    @allure.step("Select sleep routine option")
    def select_sleep_routine(self, sleep_value: str):
        """Select a sleep routine option (handles quotes safely)."""
        self.log.info(f"😴 Selecting sleep routine: {sleep_value}")

        quote, safe_text = self._escape_xpath_text(sleep_value)
        locator_str = f"//div[normalize-space(text())={quote}{safe_text}{quote}]"

        sleep_option = self.frame.locator(locator_str)
        sleep_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        sleep_option.scroll_into_view_if_needed()
        expect(sleep_option).to_be_visible(timeout=5000)
        sleep_option.click()

        self.log.info(f"✅ Selected sleep routine: {sleep_value}")

    @allure.step("Click 'Next' button on Sleep Check page")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
