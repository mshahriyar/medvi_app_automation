from playwright.sync_api import Page, expect
import logging


class MetabolicGraphPage:
    """Handles metabolic graph verification in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("MetabolicGraphPage")
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_graph(self):
        """Verify the metabolic graph is visible."""
        self.log.info("🔍 Verifying metabolic graph...")
        graph_img = self.frame.locator("img[src*='withmedvi.png']")
        expect(graph_img).to_be_visible(timeout=10000)
        self.log.info("✅ Graph verified")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
