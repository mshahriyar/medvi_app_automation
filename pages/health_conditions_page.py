from playwright.sync_api import Page, expect
import logging
import allure
from typing import List


class HealthConditionsPage:
    """Handles the 'Health Conditions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("HealthConditionsPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify health conditions page content")
    def verify_health_conditions_content(self):
        """Verify static texts on the Health Conditions page."""
        self.log.info("🔍 Verifying Health Conditions content...")

        disclaimer = self.frame.locator(
            "//p[contains(normalize-space(.), 'Your answers are completely confidential and protected by HIPAA')]"
        )
        question_text = self.frame.locator(
            "//span[contains(normalize-space(.), 'Do any of these apply to you?')]"
        )

        expect(disclaimer).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(question_text).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Health Conditions content verified successfully")

    @allure.step("Verify and select health condition options")
    def verify_and_select_conditions(self, selections: List[str]):
        """Verify visibility of all condition options, then select the given ones."""
        self.log.info("🩺 Verifying and selecting health conditions...")

        valid_conditions = [
            "End-stage liver disease (cirrhosis)",
            "End-stage kidney disease (on or about to be on dialysis)",
            "Severe gastrointestinal condition (gastroparesis, blockage, inflammatory bowel disease)",
            "Current diagnosis of or treatment for alcohol, opioid, or substance use disorder/dependence",
            "Current suicidal thoughts and/or prior suicidal attempt",
            "Cancer (active diagnosis, active treatment, or in remission or cancer-free for less than 5 continuous years - does not apply to non-melanoma skin cancer that was considered cured via simple excision)",
            "None of these",
        ]

        for selection in selections:
            if selection not in valid_conditions:
                self.log.warning(f"⚠️ Invalid condition '{selection}' (skipped)")
                continue

            quote = '"' if "'" in selection else "'"
            locator = self.frame.locator(
                f"//div[normalize-space(text())={quote}{selection}{quote}]"
            )

            try:
                locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                locator.scroll_into_view_if_needed()
                locator.click()
                self.log.info(f"✅ Selected: {selection}")
            except Exception as e:
                self.log.error(f"❌ Failed to select '{selection}': {e}")

    @allure.step("Click 'Next' button on Health Conditions page")
    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
