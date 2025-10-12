from playwright.sync_api import Page, expect
import logging
class SleepHoursPage:
    """Handles the 'Sleep Hours' step in the MEDVi Typeform flow."""
    log = logging.getLogger("SleepHoursPage")
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        # Image
        self.sleep_image = self.frame.locator(
            "img[src*='id-1tAZd12DZCus/widgetid-k1Xy/hHZFcPL7X59pJZtoxUx5JW/gallaghergallagher_Romantic_lifestyle_photography_style_warm__cdfcbe67-e11e-45d2-8ef5-2f0a6d85ca4c_3.png']"
        )

        # Question Text
        self.sleep_heading = self.frame.locator(
            "//*[normalize-space(text())='How many hours of sleep do you usually get each night?']"
        )

        # Dynamic option template (e.g., “4-5 hours”, “6-7 hours”, etc.)
        self.choose_sleep_hours_option = "//div[normalize-space(text())='{sleep_hours}']"

        # Next button
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    # -------------------- Validations --------------------

    def verify_sleep_heading_and_image(self):
        """Verify that the question text and image are visible."""
        self.log.info("Verifying sleep heading and image...")

        results = {
            "sleep_heading": expect(self.sleep_heading).to_be_visible(timeout=10000),
            "sleep_image": expect(self.sleep_image).to_be_visible(timeout=10000),
        }

        all_passed = all(results.values())

        self.log.info("\nSleep Page Validation Summary:")
        for name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log.info(f"   {name}: {status}")

        if all_passed:
            self.log.info("Sleep page heading and image verified successfully!\n")
        else:
            self.log.info("⚠️ Some elements are missing or not visible.\n")

        return all_passed

    # -------------------- Actions --------------------

    def select_sleep_hours(self, sleep_hours: str):
        """Select a sleep hours option dynamically (e.g., '6-7 hours')."""
        self.log.info(f"😴 Selecting sleep hours option: {sleep_hours}")
        try:
            locator_str = self.choose_sleep_hours_option.format(sleep_hours=sleep_hours)
            sleep_option = self.frame.locator(locator_str)

            sleep_option.wait_for(state="visible", timeout=10000)
            sleep_option.scroll_into_view_if_needed()
            sleep_option.click()
            expect(sleep_option).to_be_visible(timeout=5000)
            self.log.info(f"✅ Selected sleep hours option: {sleep_hours}")
        except Exception as e:
            self.log.info(f"❌ Failed to select sleep hours option '{sleep_hours}': {e}")
            raise

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.log.info("➡️ Clicking 'Next' button on Sleep Hours page...")
        try:
            self.next_button.wait_for(state="visible", timeout=10000)
            self.next_button.click(timeout=10000)
            self.log.info("✅ Clicked 'Next' button successfully")
        except Exception as e:
            self.log.info(f"❌ Failed to click 'Next' button: {e}")
            raise

