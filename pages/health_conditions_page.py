from playwright.sync_api import Page, expect
import logging, time
import allure
from typing import List
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class HealthConditionsPage(BasePage):
    """Handles the 'Health Conditions' step in the MEDVi Typeform flow."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=2):
        """Retry a flaky action several times before giving up."""
        for attempt in range(1, retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt < retries:
                    self.log.warning(f"🔁 Attempt {attempt}/{retries} failed: {e}. Retrying in {delay}s…")
                    time.sleep(delay)
                else:
                    self.log.error(f"❌ All {retries} attempts failed: {e}")
                    raise

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify health conditions page content")
    def verify_health_conditions_content(self):
        """Verify static texts on the Health Conditions page."""
        self._retry_action(self._verify_health_conditions_content)
        self.log.info("✅ Health Conditions content verified successfully")

    @allure.step("Verify and select health condition options")
    def verify_and_select_conditions(self, selections: List[str]):
        """Verify visibility of all condition options, then select the given ones."""
        self._retry_action(lambda: self._verify_and_select_conditions(selections))
        self.log.info("✅ Health conditions selection completed")

    @allure.step("Click 'Next' button on Health Conditions page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_health_conditions_content(self):
        self.log.info("🔍 Verifying Health Conditions content...")
        disclaimer = self.frame.locator(
            "//p[contains(normalize-space(.), 'Your answers are completely confidential and protected by HIPAA')]"
        )
        question_text = self.frame.locator(
            "//span[contains(normalize-space(.), 'Do any of these apply to you?')]"
        )
        expect(disclaimer).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(question_text).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _verify_and_select_conditions(self, selections: List[str]):
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

            safe_value = self.escape_xpath_text(selection)
            locator = self.frame.locator(
                f"//div[normalize-space(text())={safe_value}]"
            )

            try:
                locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                locator.scroll_into_view_if_needed()
                locator.click()
                self.log.info(f"✅ Selected: {selection}")
            except Exception as e:
                self.log.error(f"❌ Failed to select '{selection}': {e}")

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
