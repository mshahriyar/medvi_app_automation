from playwright.sync_api import Page, expect


class MetabolicGraphPage:
    """Handles metabolic graph verification in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def verify_graph(self):
        """Verify the metabolic graph is visible."""
        print("🔍 Verifying metabolic graph...")
        graph_img = self.frame.locator("img[src*='withmedvi.png']")
        expect(graph_img).to_be_visible(timeout=10000)
        print("✅ Graph verified")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")
