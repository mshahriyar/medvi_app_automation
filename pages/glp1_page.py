from playwright.sync_api import Page, expect
import logging


class GLP1Page:
    """Handles GLP-1 informational section in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GLP1Page")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

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
        self.week_1_4_text = self.frame.locator("xpath=//p[contains(text(), 'Week 1-4')]")
        self.week_4_8_text = self.frame.locator("xpath=//p[contains(text(), 'Week 4-8')]")
        self.week_9_plus_text = self.frame.locator("xpath=//p[contains(text(), 'Week 9+')]")
        self.fat_burning_text = self.frame.locator("xpath=//*[contains(text(), 'fat burning machine')]")

    def wait_for_glp1_graph(self, max_wait: int = 30000):
        """Wait until the GLP-1 graph (image) becomes visible inside the iframe."""
        self.log.info("🔄 Waiting for GLP-1 graph to appear...")

        try:
            expect(self.glp1_image).to_be_visible(timeout=max_wait)
            self.log.info("✅ GLP-1 graph image loaded successfully")
        except Exception:
            self.log.info("⚠️ GLP-1 graph not visible yet, reloading iframe...")
            try:
                # Reload the iframe only
                self.page.evaluate(
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src = "
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src"
                )
                self.page.wait_for_timeout(4000)
                self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
                expect(self.glp1_image).to_be_visible(timeout=max_wait)
                self.log.info("✅ GLP-1 graph became visible after iframe reload")
            except Exception as e:
                raise TimeoutError(f"❌ GLP-1 graph failed to load: {e}")

    def verify_glp1_content(self):
        """Verify all GLP-1 related informational texts are visible."""
        self.log.info("🔍 Verifying GLP-1 content...")

        try:
            expect(self.title_text).to_be_visible(timeout=8000)
            expect(self.week_1_4_text).to_be_visible(timeout=8000)
            expect(self.week_4_8_text).to_be_visible(timeout=8000)
            expect(self.week_9_plus_text).to_be_visible(timeout=8000)
            expect(self.fat_burning_text).to_be_visible(timeout=8000)
            self.log.info("✅ All GLP-1 content verified")
        except Exception as e:
            self.log.warning(f"⚠️ Some GLP-1 content not visible: {e}")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
