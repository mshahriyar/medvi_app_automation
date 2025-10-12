from playwright.sync_api import Page, expect
from config.config import BASE_URL
from pages.base_page import BasePage


class AddHeightAndWeight(BasePage):
    """Handles height and weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.get_started_link = self.page.get_by_role("link", name="AM I QUALIFIED?")
        self.feet_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        self.inches_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[2]//input")
        self.weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    # -------------------- Navigation --------------------

    def open(self):
        """Open the MEDVi base URL and ensure the page is loaded."""
        print(f"🌐 Navigating to: {BASE_URL}")
        self.page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
        expect(self.page).to_have_url(BASE_URL)
        print("✅ Home page loaded successfully")

    # -------------------- Main Actions --------------------

    def click_get_started(self):
        """Click 'AM I QUALIFIED?' and ensure iframe is ready."""
        print("🔗 Clicking 'AM I QUALIFIED?' link...")
        self.get_started_link.wait_for(state="visible", timeout=15000)
        self.get_started_link.click()
        self.wait_for_iframe_ready()

    def wait_for_iframe_ready(self, max_retries: int = 10):
        """
        Wait for the Typeform iframe to load and retry by going back
        and clicking 'AM I QUALIFIED?' again if not loaded.
        """
        iframe_selector = self.IFRAME_SELECTOR
        dropdown_locator = "(//div[@data-cy='dropdown-component'])[1]//input"

        for attempt in range(1, max_retries + 1):
            print(f"🔄 Attempt {attempt}/{max_retries}: Waiting for iframe to load...")

            try:
                # Wait for iframe to attach
                self.page.wait_for_selector(iframe_selector, state="attached", timeout=5000)
                self.frame = self.page.frame_locator(iframe_selector)

                # Wait for dropdown inside iframe
                self.frame.locator(dropdown_locator).wait_for(state="visible", timeout=10000)
                print("✅ Iframe loaded and form visible!")
                return

            except Exception as e:
                print(f"⚠️ Iframe not ready (Attempt {attempt}): {e}")

                if attempt < max_retries:
                    print("↩️ Going back and retrying...")
                    try:
                        self.page.go_back(wait_until="domcontentloaded", timeout=10000)
                        self.page.wait_for_timeout(2000)

                        # Retry clicking the link
                        link = self.page.get_by_role("link", name="AM I QUALIFIED?")
                        link.wait_for(state="visible", timeout=10000)
                        link.click()
                        self.page.wait_for_timeout(3000)

                    except Exception as nav_error:
                        print(f"❌ Retry navigation failed: {nav_error}")
                else:
                    print("❌ Max retries reached. Iframe still not loaded.")
                    raise TimeoutError("Iframe failed to load after multiple retries.") from e

    # -------------------- Form Actions --------------------

    def select_feet(self, value: str):
        """Select feet from dropdown."""
        print(f"🦶 Selecting feet: {value}")
        self._select_from_dropdown(self.feet_dropdown, value, 1)

    def select_inches(self, value: str):
        """Select inches from dropdown."""
        print(f"📏 Selecting inches: {value}")
        self._select_from_dropdown(self.inches_dropdown, value, 2)

    def add_weight(self, weight: str):
        """Enter weight value."""
        print(f"⚖️ Entering weight: {weight}")
        self.weight_input.wait_for(state="visible", timeout=10000)
        self.weight_input.fill(weight)
        expect(self.weight_input).to_have_value(weight)
        print("✅ Weight entered successfully")

    def hit_next_button(self):
        """Click the 'Next' button."""
        self.next_button.wait_for(state="visible", timeout=10000)
        self.next_button.click()
        print("➡️ Clicked 'Next' button")

    # -------------------- Utility --------------------

    def _select_from_dropdown(self, dropdown, value: str, index: int):
        """Reusable dropdown selector."""
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.click()
        dropdown.fill(value)
        self.page.keyboard.press("Enter")

        selected_option = self.frame.locator(
            f"(//div[@data-cy='dropdown-component'])[{index}]//div[contains(text(), '{value}')]"
        )
        expect(selected_option).to_be_visible(timeout=5000)
        print(f"✅ Selected '{value}' from dropdown {index}")
