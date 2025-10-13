from playwright.sync_api import Page, expect
import logging
import allure


class GLP1Page:
    """Handles GLP-1 informational section in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GLP1Page")

    @property
    def frame(self):
        """Always get a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Wait for GLP-1 graph to appear")
    def wait_for_glp1_graph(self, max_wait: int = 30000):
        """Wait until the GLP-1 graph (image) becomes visible inside the iframe."""
        self.log.info("🔄 Waiting for GLP-1 graph to appear...")

        glp1_image = self.frame.locator(
            "img[src*='ChatGPT-Image-Mar-27-2025-01_16_53-PM.png']"
        )
        try:
            expect(glp1_image).to_be_visible(timeout=max_wait)
            self.log.info("✅ GLP-1 graph image loaded successfully")
        except Exception as e:
            self.log.warning(f"⚠️ GLP-1 graph not visible yet: {e}. Reloading iframe…")
            try:
                self.page.evaluate(
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src = "
                    f"document.querySelector('{self.IFRAME_SELECTOR}').src"
                )
                self.page.wait_for_timeout(4000)
                expect(glp1_image).to_be_visible(timeout=max_wait)
                self.log.info("✅ GLP-1 graph became visible after iframe reload")
            except Exception as reload_error:
                msg = f"❌ GLP-1 graph failed to load after reload: {reload_error}"
                self.log.error(msg)
                raise TimeoutError(msg)

    @allure.step("Verify GLP-1 informational content")
    def verify_glp1_content(self):
        """Verify all GLP-1 related informational texts are visible."""
        self.log.info("🔍 Verifying GLP-1 informational content...")

        elements = [
            self.frame.locator("text=How will GLP-1 work for you?"),
            self.frame.locator("xpath=//p[contains(text(), 'Week 1-4')]"),
            self.frame.locator("xpath=//p[contains(text(), 'Week 4-8')]"),
            self.frame.locator("xpath=//p[contains(text(), 'Week 9+')]"),
        ]

        missing = []
        for el in elements:
            try:
                expect(el).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
            except Exception as e:
                missing.append(str(e))

        if missing:
            self.log.warning(f"⚠️ Some GLP-1 content not visible:\n" + "\n".join(missing))
        else:
            self.log.info("✅ All GLP-1 content verified")

    @allure.step("Click 'Next' button on GLP-1 page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
