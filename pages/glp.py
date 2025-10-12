from playwright.sync_api import Page, expect
import logging
class GPL1Page:
    """Handles GLP-1 informational section in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    log = logging.getLogger("GPL1Page")
    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

        # GLP-1 image and heading
        self.glp1_image = self.frame.locator(
            "img[src*='ChatGPT-Image-Mar-27-2025-01_16_53-PM.png']"
        )
        self.glp1_heading = self.frame.locator(
            "xpath=//span[contains(text(), 'How will GLP-1')] | //em[contains(text(), 'GLP-1')]"
        )

        # GLP-1 descriptive texts
        self.title_text = self.frame.locator("text=How will GLP-1 work for you?")
        self.week_1_4_text = self.frame.locator(
            "xpath=//p[contains(text(), 'Week 1-4')]"
        )
        self.week_4_8_text = self.frame.locator(
            "xpath=//p[contains(text(), 'Week 4-8')]"
        )
        self.week_9_plus_text = self.frame.locator(
            "xpath=//p[contains(text(), 'Week 9+')]"
        )
        self.fat_burning_text = self.frame.locator(
            "xpath=//*[contains(text(), 'fat burning machine')]"
        )

    # -------------------- Iframe Handling --------------------

    def wait_for_glp1_graph(self, max_wait: int = 30000):
        """
        Wait until the GLP-1 graph (image) becomes visible inside the iframe.
        If it doesn't load, reload only the iframe once.
        """
        self.log.info("Waiting for GLP-1 graph to appear...")

        try:
            expect(self.glp1_image).to_be_visible(timeout=max_wait)
            self.log.info("GLP-1 graph image loaded successfully")
        except Exception:
            self.log.info("GLP-1 graph not visible yet, reloading only iframe...")
            try:
                # Reload the iframe only (not the whole page)
                self.page.evaluate(
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src = "
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src"
                )
                self.page.wait_for_timeout(4000)
                self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
                expect(self.glp1_image).to_be_visible(timeout=max_wait)
                self.log.info("GLP-1 graph became visible after iframe reload")
            except Exception as e:
                raise TimeoutError(f"❌ GLP-1 graph failed to load after waiting: {e}")

    # -------------------- Validation Methods --------------------

    def verify_glp1_heading_visible(self):
        """Verify the GLP-1 heading text is visible."""
        self.log.info("Verifying GLP-1 heading text...")
        expect(self.glp1_heading.first).to_be_visible(timeout=10000)
        self.log.info("GLP-1 heading text is visible")

    def verify_glp1_content(self):
        """Verify all GLP-1 related informational texts are visible."""
        self.log.info("Verifying GLP-1 informational content...")

        validation_results = {
            "title_text": self._is_visible(self.title_text, "How will GLP-1 work for you?"),
            "week_1_4_text": self._is_visible(
                self.week_1_4_text, "Week 1-4: Your body gets acclimated to GLP-1 medication"
            ),
            "week_4_8_text": self._is_visible(
                self.week_4_8_text, "Week 4-8: Weight loss is increasing more and more"
            ),
            "week_9_plus_text": self._is_visible(
                self.week_9_plus_text, "Week 9+: Your body has become a"
            ),
            "fat_burning_text": self._is_visible(
                self.fat_burning_text, "fat burning machine"
            ),
        }

        all_passed = all(validation_results.values())

        self.log.info("\nGLP-1 Content Validation Summary:")
        for name, result in validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log.info(f"   {name}: {status}")

        if all_passed:
            self.log.info("\nAll GLP-1 content texts are visible and validated successfully!")
        else:
            self.log.info("\nSome GLP-1 content texts are missing or not visible!")

        return all_passed

    def _is_visible(self, locator, description: str) -> bool:
        """Utility function to safely check if a locator is visible."""
        try:
            expect(locator.first).to_be_visible(timeout=8000)
            self.log.info(f"✅ '{description}' is visible")
            return True
        except Exception as e:
            self.log.info(f"❌ '{description}' not visible → {e}")
            return False

    # -------------------- Action Methods --------------------

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.log.info("Clicking 'Next' button...")
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click(timeout=10000)
        self.log.info("Clicked 'Next' button successfully")
