from playwright.sync_api import Page, expect
import logging
class HealthConditionsPage:
    """Handles the 'Health Conditions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("HealthConditionsPage")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.confidential_disclaimer = self.frame.locator(
            "//p[contains(normalize-space(.), 'Your answers are completely confidential and protected by HIPAA')]"
        )
        self.apply_to_you_text = self.frame.locator(
            "//span[contains(normalize-space(.), 'Do any of these apply to you?')]"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # --- Condition text list ---
        self.conditions = [
            "End-stage liver disease (cirrhosis)",
            "End-stage kidney disease (on or about to be on dialysis)",
            "Severe gastrointestinal condition (gastroparesis, blockage, inflammatory bowel disease)",
            "Current diagnosis of or treatment for alcohol, opioid, or substance use disorder/dependence",
            "Current suicidal thoughts and/or prior suicidal attempt",
            "Cancer (active diagnosis, active treatment, or in remission or cancer-free for less than 5 continuous years - does not apply to non-melanoma skin cancer that was considered cured via simple excision)",
            "None of these"
        ]

    # -------------------- Page Validations --------------------

    def verify_health_conditions_content(self):
        """Verify static texts on the Health Conditions page."""
        self.log.info("Verifying 'Health Conditions' page content...")

        validation_results = {}

        for name, locator in {
            "confidential_disclaimer": self.confidential_disclaimer,
            "apply_to_you_text": self.apply_to_you_text,
        }.items():
            try:
                expect(locator).to_be_visible(timeout=10000)
                self.log.info(f"✅ Visible: {name}")
                validation_results[name] = True
            except Exception as e:
                self.log.info(f"❌ Not visible: {name} → {e}")
                validation_results[name] = False

        all_passed = all(validation_results.values())

        self.log.info("\nHealth Conditions Page Validation Summary:")
        for name, result in validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log.info(f"   {name}: {status}")

        return all_passed

    # -------------------- Verification + Selection --------------------

    def verify_and_select_conditions(self, selections: list[str]):
        """
        Verify visibility of all condition options, then select the given ones.
        Automatically handles apostrophes and skips invalid entries.
        """
        self.log.info("\nVerifying visibility of all medical condition options...")

        # --- Verify all available condition options ---
        for condition in self.conditions:
            quote = '"' if "'" in condition else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{condition}{quote}]")

            try:
                expect(locator).to_be_visible(timeout=8000)
                self.log.info(f"✅ Visible: {condition}")
            except Exception as e:
                self.log.info(f"⚠️ Not visible: {condition} → {e}")

        print("\n🩺 Selecting medical conditions as per test data...")

        # --- Select specified options ---
        for selection in selections:
            if selection not in self.conditions:
                self.log.info(f"⚠️ Invalid condition '{selection}' (skipped)")
                continue

            quote = '"' if "'" in selection else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{selection}{quote}]")

            try:
                locator.wait_for(state="visible", timeout=8000)
                locator.scroll_into_view_if_needed()
                locator.click()
                self.log.info(f"✅ Selected: {selection}")
            except Exception as e:
                self.log.info(f"❌ Failed to select '{selection}' → {e}")


    def hit_next_button(self):
        """Click the 'Next' button."""
        self.log.info("Clicking next button...")
        self.next_button.click()
        self.log.info("Next button clicked")
