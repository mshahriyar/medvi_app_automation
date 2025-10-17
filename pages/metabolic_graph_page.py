from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class MetabolicGraphPage(BasePage):
    """Handles metabolic graph verification in the MEDVi Typeform flow."""

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

    @allure.step("Verify metabolic graph content is visible")
    def verify_metabolic_graph_content_visible(self):
        """Verify the metabolic graph content is visible."""
        self.log.info("🔍 Verifying metabolic graph content is visible...")
        content = self.frame.locator("//*[normalize-space(text())='metabolic science.']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Metabolic graph content is visible verified successfully")

    @allure.step("Verify metabolic graph is visible")
    def verify_graph(self):
        """Verify the metabolic graph image is visible inside the iframe."""
        self._retry_action(self._verify_graph)
        self.log.info("✅ Metabolic graph verified successfully")

    @allure.step("Click 'Next' button on Metabolic Graph page")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _verify_graph(self):
        self.log.info("🔍 Verifying metabolic graph...")
        graph_img = self.frame.locator("img[src*='withmedvi.png']")
        expect(graph_img).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
