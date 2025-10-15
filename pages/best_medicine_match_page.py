from playwright.sync_api import Page, expect
import logging
import allure


class BestMedicineMatchPage:
    """Handles 'Best Medicine Match' step interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("BestMedicineMatchPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Utility ---------------------- #
    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath — handles both single and double quotes."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # ---------------------- Actions ---------------------- #
    @allure.step("Verify best medicine match heading")
    def verify_best_medicine_match_heading(self):
        """Verify the best medicine match heading is visible."""
        self.log.info("🔍 Verifying best medicine match heading...")
        heading = self.frame.locator("//span[text()='Which of these is most important to you?']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Best medicine match heading verified successfully")

    @allure.step("Select best medicine match option")
    def select_best_medicine_match(self, best_medicine_match_value: str):
        """Select a best medicine match option dynamically based on provided value."""
        clean_value = best_medicine_match_value.strip()
        safe_value = self.escape_xpath_text(clean_value)
        self.log.info(f"🩺 Selecting best medicine match: '{clean_value}'")

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

    @allure.step("Select GLP-1 tablet or injection")
    def select_glp1_tablet_or_injection(self, glp1_tablet_or_injection_value: str):
        """Select a GLP-1 tablet or injection option dynamically based on provided value."""
        self.log.info("🔍 Verifying GLP-1 tablet or injection heading...")
        heading2 = self.frame.locator(
            "//span[text()='GLP-1 is available as an injection or a dissolvable tablet. Which sounds best?']"
        )
        expect(heading2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ GLP-1 tablet or injection heading verified successfully")

        clean_value = glp1_tablet_or_injection_value.strip()
        safe_value = self.escape_xpath_text(clean_value)
        self.log.info(f"💉 Selecting GLP-1 tablet or injection: '{clean_value}'")

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
