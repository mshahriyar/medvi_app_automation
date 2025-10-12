from playwright.sync_api import Page, expect


class SleepHoursPage:
    """Handles the 'Sleep Hours' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Image
        self.sleep_image = self.frame.locator(
            "img[src*='id-1tAZd12DZCus/widgetid-k1Xy/hHZFcPL7X59pJZtoxUx5JW/gallaghergallagher_Romantic_lifestyle_photography_style_warm__cdfcbe67-e11e-45d2-8ef5-2f0a6d85ca4c_3.png']"
        )

        # Question Text
        self.sleep_heading = self.frame.locator(
            "//*[normalize-space(text())='How many hours of sleep do you usually get each night?']"
        )

        # Dynamic option template
        self.choose_sleep_hours_option = "//div[normalize-space(text())='{sleep_hours}']"

        # Next button
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_sleep_heading_and_image(self):
        """Verify that the question text and image are visible."""
        print("🔍 Verifying sleep heading and image...")
        expect(self.sleep_heading).to_be_visible(timeout=10000)
        expect(self.sleep_image).to_be_visible(timeout=10000)
        print("✅ Sleep heading and image verified")

    def select_sleep_hours(self, sleep_hours: str):
        """Select a sleep hours option dynamically."""
        print(f"😴 Selecting sleep hours option: {sleep_hours}")

        locator_str = self.choose_sleep_hours_option.format(sleep_hours=sleep_hours)
        sleep_option = self.frame.locator(locator_str)

        sleep_option.wait_for(state="visible", timeout=10000)
        sleep_option.scroll_into_view_if_needed()
        sleep_option.click()
        expect(sleep_option).to_be_visible(timeout=5000)
        print(f"✅ Selected sleep hours option: {sleep_hours}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
