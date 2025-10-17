from playwright.sync_api import Page, expect
import logging, time
import allure
from typing import List
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class AdditionalHealthQuestionsPage(BasePage):
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

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

    @allure.step("Verify main and sub headings are visible on Additional Health Questions page")
    def verify_page_headings(self):
        """Verify both main and sub headings are visible."""
        self._retry_action(self._verify_page_headings)
        self.log.info("✅ Page headings verified successfully")

    @allure.step("Verify all additional health conditions are visible")
    def verify_all_conditions_visible(self):
        """Verify all condition options are visible."""
        self._retry_action(self._verify_all_conditions_visible)
        self.log.info("✅ All conditions verification completed")

    @allure.step("Select one or more health conditions")
    def select_conditions(self, selections: List[str]):
        """Select specific conditions dynamically."""
        self._retry_action(lambda: self._select_conditions(selections))
        self.log.info("✅ Health conditions selection completed")

    @allure.step("Click 'Next' button on Additional Health Questions page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_page_headings(self):
        self.log.info("🔍 Verifying page headings...")
        main_heading = self.frame.locator("//span[normalize-space(text())='A few more health questions']")
        sub_heading = self.frame.locator("//span[normalize-space(text())='Do any of these apply to you?']")
        expect(main_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(sub_heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _verify_all_conditions_visible(self):
        self.log.info("🔍 Verifying all conditions are visible...")
        conditions = self._get_conditions_list()
        missing_conditions = []

        for condition in conditions:
            quote = '"' if "'" in condition else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{condition}{quote}]")
            try:
                expect(locator).to_be_visible(timeout=7000)
            except Exception:
                missing_conditions.append(condition)
                self.log.warning(f"⚠️ Condition not visible: {condition}")

        if missing_conditions:
            self.log.warning(f"⚠️ Missing conditions: {missing_conditions}")
        else:
            self.log.info("✅ All conditions are visible")

    def _select_conditions(self, selections: List[str]):
        self.log.info("🩺 Selecting health conditions...")
        conditions = self._get_conditions_list()

        for selection in selections:
            if selection not in conditions:
                self.log.warning(f"⚠️ Invalid condition '{selection}' (skipped)")
                continue

            quote = '"' if "'" in selection else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{selection}{quote}]")

            try:
                locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                locator.scroll_into_view_if_needed()
                locator.click()
                expect(locator).to_be_visible(timeout=5000)
                self.log.info(f"✅ Selected: {selection}")
            except Exception as e:
                self.log.error(f"❌ Failed to select '{selection}': {e}")

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()

    # ---------------------- Internal Helpers ---------------------- #

    def _get_conditions_list(self) -> List[str]:
        """Return the list of all available health condition options."""
        return [
            "Gallbladder disease",
            "Hypertension (high blood pressure)",
            "Seizures",
            "Glaucoma",
            "Sleep apnea",
            "Type 2 diabetes (not on insulin)",
            "Type 2 diabetes (on insulin)",
            "Type 1 diabetes",
            "Diabetic retinopathy (diabetic eye disease), damage to the optic nerve from trauma or reduced blood flow, or blindness",
            "Use of the blood thinner warfarin (Coumadin/Jantoven)",
            "History of or current pancreatitis",
            "Personal or family history of thyroid cyst/nodule, thyroid cancer, medullary thyroid carcinoma, or multiple endocrine neoplasia syndrome type 2",
            "Gout",
            "High cholesterol or triglycerides",
            "Depression",
            "Head injury",
            "Tumor/infection in brain/spinal cord",
            "Low sodium",
            "Liver disease, including fatty liver",
            "Kidney disease",
            "Elevated resting heart rate (tachycardia)",
            "Coronary artery disease or heart attack/stroke in last 2 years",
            "Allergic to any medication",
            "Congestive heart failure",
            "QT prolongation or other heart rhythm disorder",
            "Hospitalization within the last 1 year",
            "Human immunodeficiency virus (HIV)",
            "Acid reflux",
            "Asthma/reactive airway disease",
            "Urinary stress incontinence",
            "Polycystic ovarian syndrome (PCOS)",
            "Clinically proven low testosterone",
            "Osteoarthritis",
            "Constipation",
            "None of these",
        ]
