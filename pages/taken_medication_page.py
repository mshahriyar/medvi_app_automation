# These are three options i have:

# option1: Yes, I've taken GLP-1 medication
# option2: Yes, I've taken a different medication for weight loss
# option3: No

# h2: Have you taken medication for weight loss within the past 4 weeks?

from playwright.sync_api import Page, expect
import logging
import allure


class TakenMedicationPage:
    """Handles 'Taken Medication' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("TakenMedicationPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    def escape_xpath_text(self, text: str) -> str:
        """
        Safely escape text for XPath — handles both single and double quotes.
        Example: "Yes, I've taken" → concat('Yes, I', "'", 've taken')
        """
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"


    @allure.step("Select taken medication option")
    def select_taken_medication(self, taken_medication_value: str):
        """Select a 'taken medication' option dynamically and verify its border color."""
        clean_value = taken_medication_value.strip()
        self.log.info(f"💊 Selecting taken medication: '{clean_value}'")

        # Build safe XPath for text with quotes
        safe_value = self.escape_xpath_text(clean_value)
        option_locator = self.frame.locator(f"xpath=//div[normalize-space(text())={safe_value}]")

        try:
            # Wait for and click the main option
            option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            option_locator.scroll_into_view_if_needed()
            expect(option_locator).to_be_visible(timeout=5000)
            option_locator.click()
            self.log.info(f"✅ Option clicked: '{clean_value}'")

            # Locate the radio or highlight span and get computed border color
            radio = self.frame.locator(
                f"xpath=//div[normalize-space(text())={safe_value}]/../../preceding-sibling::span"
            )
            border_color = radio.evaluate("el => getComputedStyle(el).borderColor")
            self.log.info(f"🎨 Detected border color: {border_color}")

            # ✅ Corrected: compare as string, not with expect()
            assert border_color == "rgb(198, 166, 115)", (
                f"❌ Border color mismatch for '{clean_value}': {border_color}"
            )

            self.log.info(f"✅ Successfully selected and verified: '{clean_value}'")

        except Exception as e:
            msg = f"❌ Failed to select '{clean_value}': {e}"
            self.log.error(msg)
            raise RuntimeError(msg)
    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")


