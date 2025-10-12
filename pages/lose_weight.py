from playwright.sync_api import Page, expect
import logging
class LoseWeightPage:
    """Handles the 'Lose Weight' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("LoseWeightPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.lose_weight_heading = self.frame.locator(
            "//span[contains(normalize-space(.), \"With medication, you'll lose 3 to 4 pounds\")]"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    # -------------------- Utility --------------------

    def _escape_xpath_text(self, text: str) -> str:
        """
        Escape quotes in XPath-safe format.
        Handles cases like: That's too fast → concat('That', "'", 's too fast')
        """
        if "'" not in text:
            return f"'{text}'"
        elif '"' not in text:
            return f'"{text}"'
        else:
            parts = text.split("'")
            return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # -------------------- Actions --------------------

    def select_lose_weight(self, lose_weight_value: str):
        """Select an option for how fast the user wants to lose weight."""
        self.log.info(f"Selecting lose weight option: {lose_weight_value}")
        try:
            # Escape text safely for XPath
            safe_value = self._escape_xpath_text(lose_weight_value)
            locator_str = f"//div[normalize-space(text())={safe_value}]"
            weight_option = self.frame.locator(locator_str)

            # Wait for element and click
            weight_option.wait_for(state="visible", timeout=10000)
            weight_option.scroll_into_view_if_needed()
            expect(weight_option).to_be_visible(timeout=5000)
            weight_option.click()

            self.log.info(f"✅ Selected lose weight option: {lose_weight_value}")
        except Exception as e:
            self.log.info(f"❌ Failed to select lose weight option '{lose_weight_value}': {e}")
            raise

    def verify_lose_weight_heading(self):
        """Verify that the lose weight heading text is visible."""
        self.log.info("Verifying lose weight heading text...")
        try:
            expect(self.lose_weight_heading).to_be_visible(timeout=10000)
            self.log.info("✅ Heading 'With medication, you'll lose 3 to 4 pounds' is visible")
        except Exception as e:
            self.log.info(f"❌ Lose weight heading not visible or mismatched: {e}")
            raise

    def hit_next_button(self):
        """Click the 'Next' button after selecting lose weight option."""
        self.log.info("Clicking 'Next' button on Lose Weight page...")
        try:
            self.next_button.wait_for(state="visible", timeout=10000)
            self.next_button.click(timeout=10000)
            self.log.info("✅ Clicked 'Next' button successfully")
        except Exception as e:
            self.log.info(f"❌ Failed to click 'Next' button: {e}")
            raise
