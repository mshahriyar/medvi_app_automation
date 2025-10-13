from playwright.sync_api import Page, expect
import logging
import allure


class LoseWeightPage:
    """Handles the 'Lose Weight' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("LoseWeightPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Helpers ---------------------- #

    def _escape_xpath_text(self, text: str) -> str:
        """Escape quotes in XPath-safe format."""
        if "'" not in text:
            return f"'{text}'"
        elif '"' not in text:
            return f'"{text}"'
        else:
            parts = text.split("'")
            return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # ---------------------- Actions ---------------------- #

    @allure.step("Select lose weight option")
    def select_lose_weight(self, lose_weight_value: str):
        """Select an option for how fast the user wants to lose weight."""
        self.log.info(f"⚖️ Selecting lose weight option: {lose_weight_value}")

        safe_value = self._escape_xpath_text(lose_weight_value)
        locator_str = f"//div[normalize-space(text())={safe_value}]"
        option = self.frame.locator(locator_str)

        option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option.scroll_into_view_if_needed()
        expect(option).to_be_visible(timeout=5000)
        option.click()

        self.log.info(f"✅ Selected lose weight option: {lose_weight_value}")

    @allure.step("Verify lose weight heading")
    def verify_lose_weight_heading(self):
        """Verify that the lose weight heading text is visible."""
        self.log.info("🔍 Verifying lose weight heading...")

        heading = self.frame.locator(
            "//span[contains(normalize-space(.), \"With medication, you'll lose 3 to 4 pounds\")]"
        )
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Lose weight heading visible")

    @allure.step("Click 'Next' button on Lose Weight page")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
