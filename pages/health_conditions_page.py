from playwright.sync_api import Page, expect
import logging


class HealthConditionsPage:
    """Handles the 'Health Conditions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("HealthConditionsPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        self.confidential_disclaimer = self.frame.locator(
            "//p[contains(normalize-space(.), 'Your answers are completely confidential and protected by HIPAA')]"
        )
        self.apply_to_you_text = self.frame.locator(
            "//span[contains(normalize-space(.), 'Do any of these apply to you?')]"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # Condition text list
        self.conditions = [
            "End-stage liver disease (cirrhosis)",
            "End-stage kidney disease (on or about to be on dialysis)",
            "Severe gastrointestinal condition (gastroparesis, blockage, inflammatory bowel disease)",
            "Current diagnosis of or treatment for alcohol, opioid, or substance use disorder/dependence",
            "Current suicidal thoughts and/or prior suicidal attempt",
            "Cancer (active diagnosis, active treatment, or in remission or cancer-free for less than 5 continuous years - does not apply to non-melanoma skin cancer that was considered cured via simple excision)",
            "None of these"
        ]

    def verify_health_conditions_content(self):
        """Verify static texts on the Health Conditions page."""
        self.log.info("🔍 Verifying health conditions content...")
        expect(self.confidential_disclaimer).to_be_visible(timeout=10000)
        expect(self.apply_to_you_text).to_be_visible(timeout=10000)
        self.log.info("✅ Health conditions content verified")

    def verify_and_select_conditions(self, selections: list[str]):
        """Verify visibility of all condition options, then select the given ones."""
        self.log.info("🔍 Verifying and selecting health conditions...")

        # Select specified options
        for selection in selections:
            if selection not in self.conditions:
                self.log.warning(f"⚠️ Invalid condition '{selection}' (skipped)")
                continue

            quote = '"' if "'" in selection else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{selection}{quote}]")

            try:
                locator.wait_for(state="visible", timeout=8000)
                locator.scroll_into_view_if_needed()
                locator.click()
                self.log.info(f"✅ Selected: {selection}")
            except Exception as e:
                self.log.error(f"❌ Failed to select '{selection}': {e}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
