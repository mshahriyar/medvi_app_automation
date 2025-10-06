from playwright.sync_api import Page, expect

class RankPage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)


    def verify_rank(self):
        img = self.frame.locator("img[src*='forbes-number-1.png']")
        
        expect(img).to_be_visible(timeout=10000)

    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.next_button.click(timeout=10000)