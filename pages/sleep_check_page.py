from playwright.sync_api import Page, expect
import logging


class SleepCheckPage:
    """Handles the 'Sleep Check' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("SleepCheckPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")
        self.sleep_routine_heading = self.frame.locator(
            "//span[contains(normalize-space(.), 'How you sleep tells us a lot about your')]"
        )
        self.sleep_routine_selection_template = "//div[normalize-space(text())={quote}{sleep}{quote}]"

    def verify_sleep_routine_heading_visible(self):
        """Verify that the sleep routine heading is visible."""
        self.log.info("🔍 Verifying sleep routine heading...")
        expect(self.sleep_routine_heading).to_be_visible(timeout=10000)
        self.log.info("✅ Sleep routine heading visible")

    def select_sleep_routine(self, sleep_value: str):
        """Select a sleep routine option (handles quotes safely)."""
        self.log.info(f"😴 Selecting sleep routine: {sleep_value}")

        # Handle apostrophes correctly
        quote = '"' if "'" in sleep_value else "'"
        locator_str = self.sleep_routine_selection_template.format(sleep=sleep_value, quote=quote)

        sleep_option = self.frame.locator(locator_str)
        sleep_option.wait_for(state="visible", timeout=10000)
        sleep_option.scroll_into_view_if_needed()
        sleep_option.click()
        expect(sleep_option).to_be_visible(timeout=5000)
        self.log.info(f"✅ Selected sleep routine: {sleep_value}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
