from playwright.sync_api import Page, expect
from config.config import BASE_URL


class HomePage:
    """Handles navigation to MEDVi website and clicking the qualification button."""

    def __init__(self, page: Page):
        self.page = page
        self.get_started_link = self.page.get_by_role("link", name="AM I QUALIFIED?")

    def open(self):
        """Open the MEDVi base URL and ensure the page is loaded."""
        print(f"🌐 Navigating to: {BASE_URL}")
        self.page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
        expect(self.page).to_have_url(BASE_URL)
        print("✅ Home page loaded successfully")

    def click_get_started(self):
        """Click 'AM I QUALIFIED?' and wait for navigation."""
        print("🔗 Clicking 'AM I QUALIFIED?' link...")
        self.get_started_link.wait_for(state="visible", timeout=15000)
        self.get_started_link.click()
        print("✅ Clicked 'AM I QUALIFIED?' button")
