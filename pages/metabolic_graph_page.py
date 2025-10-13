from playwright.sync_api import Page, expect
import logging
import allure


class MetabolicGraphPage:
    """Handles metabolic graph verification in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("MetabolicGraphPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Verify metabolic graph is visible")
    def verify_graph(self):
        """Verify the metabolic graph image is visible inside the iframe."""
        self.log.info("🔍 Verifying metabolic graph...")

        graph_img = self.frame.locator("img[src*='withmedvi.png']")
        expect(graph_img).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        self.log.info("✅ Metabolic graph verified successfully")

    @allure.step("Click 'Next' button on Metabolic Graph page")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
