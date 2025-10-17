from playwright.sync_api import Page, expect
from config.config import BASE_URL
import logging, time
import allure


class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("HomePage")

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=3):
        """Generic retry wrapper for any flaky UI interaction."""
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

    # ----------------------- Actions -----------------------

    @allure.step("Open MEDVi home page")
    def open(self):
        """Open the MEDVi base URL and verify page load."""
        self.log.info(f"🌐 Navigating to: {BASE_URL}")
        self.page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
        expect(self.page).to_have_url(BASE_URL)
        self.log.info("✅ Home page loaded successfully")

    @allure.step("Click 'AM I QUALIFIED?' button")
    def click_get_started(self):
        """Click the 'AM I QUALIFIED?' link and handle any flakiness."""
        link = lambda: self.page.get_by_role("link", name="AM I QUALIFIED?")

        def click_link():
            link().wait_for(state="visible", timeout=15000)
            link().click()
            self.log.info("✅ Clicked 'AM I QUALIFIED?' button")

        # Retry click a few times (for network or rendering delays)
        self._retry_action(click_link, retries=3, delay=3)
