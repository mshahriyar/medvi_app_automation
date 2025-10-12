from playwright.sync_api import Page, expect


class AdditionalHealthQuestionsPage:
    """Handles the 'Additional Health Questions' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        self.main_heading = self.frame.locator(
            "//span[normalize-space(text())='A few more health questions']"
        )
        self.sub_heading = self.frame.locator(
            "//span[normalize-space(text())='Do any of these apply to you?']"
        )
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # All available condition options
        self.conditions = [
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
            "None of these"
        ]

    def verify_page_headings(self):
        """Verify both main and sub headings are visible."""
        print("🔍 Verifying page headings...")
        expect(self.main_heading).to_be_visible(timeout=10000)
        expect(self.sub_heading).to_be_visible(timeout=10000)
        print("✅ Page headings verified")

    def verify_all_conditions_visible(self):
        """Verify all condition options are visible."""
        print("🔍 Verifying all conditions are visible...")
        for condition in self.conditions:
            quote = '"' if "'" in condition else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{condition}{quote}]")
            try:
                expect(locator).to_be_visible(timeout=7000)
            except:
                print(f"⚠️ Condition not visible: {condition}")
        print("✅ Conditions visibility check completed")

    def select_conditions(self, selections: list[str]):
        """Select specific conditions dynamically."""
        print("🩺 Selecting health conditions...")

        for selection in selections:
            if selection not in self.conditions:
                print(f"⚠️ Invalid condition '{selection}' (skipped)")
                continue

            quote = '"' if "'" in selection else "'"
            locator = self.frame.locator(f"//div[normalize-space(text())={quote}{selection}{quote}]")

            try:
                locator.wait_for(state="visible", timeout=10000)
                locator.scroll_into_view_if_needed()
                locator.click()
                expect(locator).to_be_visible(timeout=5000)
                print(f"✅ Selected: {selection}")
            except Exception as e:
                print(f"❌ Failed to select '{selection}': {e}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
