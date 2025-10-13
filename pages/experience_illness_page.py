from playwright.sync_api import Page, expect
import logging
import allure


class ExperienceIllnessPage:
    """Handles 'Experience Illness' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("ExperienceIllnessPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #
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

    @allure.step("Select experience illness option")
    def select_experience_illness(self, experience_illness_value: str):
        """Select an illness option dynamically based on provided value."""
        clean_value = experience_illness_value.strip()
        self.log.info(f"🩺 Selecting experience illness: '{clean_value}'")

        safe_value = self.escape_xpath_text(clean_value)
        option_locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")

        try:
            option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            option_locator.scroll_into_view_if_needed()
            expect(option_locator).to_be_visible(timeout=5000)
            option_locator.click()
            self.log.info(f"✅ Successfully selected: '{clean_value}'")
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

