from playwright.sync_api import Page, expect
from config.config import BASE_URL


class AddHeightAndWeight:
    """Handles height and weight form interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe"

    def __init__(self, page: Page):
        self.page = page
        self.frame = None  # will be assigned dynamically after load

    # -------------------- Navigation --------------------

    def open(self):
        """Navigate to MEDVi base URL."""
        self.page.goto(BASE_URL, timeout=30000, wait_until="networkidle")

    # -------------------- Interactions --------------------

    def click_get_started(self):
        """Click the 'AM I QUALIFIED?' link."""
        self.page.get_by_role("link", name="AM I QUALIFIED?").click(timeout=10000)

    # -------------------- Iframe Handling --------------------

    def wait_for_iframe_ready(self, max_retries: int = 3):
        """
        Wait for the Typeform iframe to load and its dropdown to become visible.
        Retries automatically if iframe loads slowly.
        """
        for attempt in range(1, max_retries + 1):
            try:
                # Wait for iframe to be attached in the DOM
                self.page.wait_for_selector(self.IFRAME_SELECTOR, state="attached", timeout=20000)

                # Small buffer for Typeform rendering delay
                self.page.wait_for_timeout(3000)

                # Get the correct iframe (Typeform usually has "typeform" in its URL)
                frames = self.page.frames
                target_frame = None
                for f in frames:
                    if "typeform" in (f.url or "").lower() or "medvi" in (f.url or "").lower():
                        target_frame = f
                        break

                if not target_frame:
                    raise Exception("Typeform iframe not found in attempt", attempt)

                # Assign frame locator for interactions
                self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

                # Wait for the first dropdown input to become visible
                dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
                dropdown.wait_for(state="visible", timeout=15000)

                print(f"✅ Iframe ready on attempt {attempt}")
                return  # success — exit retry loop

            except Exception as e:
                print(f"⚠️ Iframe load attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    raise
                self.page.wait_for_timeout(3000)  # wait before retry

    # -------------------- Dropdown & Form Helpers --------------------

    def _select_from_dropdown(self, dropdown, value: str, index: int):
        """Reusable dropdown selection with built-in waiting & validation."""
        dropdown.wait_for(state="visible", timeout=15000)
        dropdown.click(timeout=10000)
        dropdown.fill(value)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(2000)

        selected_option = self.frame.locator(
            f"(//div[@data-cy='dropdown-component'])[{index}]//div[contains(text(), '{value}')]"
        )
        expect(selected_option).to_be_visible(timeout=5000)

    def select_feet(self, value: str):
        """Select 'Feet' value from dropdown."""
        feet_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        self._select_from_dropdown(feet_dropdown, value, 1)

    def select_inches(self, value: str):
        """Select 'Inches' value from dropdown."""
        inches_dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[2]//input")
        self._select_from_dropdown(inches_dropdown, value, 2)

    def add_weight(self, weight: str):
        """Enter weight (lbs) into the input field."""
        weight_input = self.frame.locator("(//input[@data-cy='input-component'])[1]")
        weight_input.wait_for(state="visible", timeout=10000)
        weight_input.fill(weight)
        expect(weight_input).to_have_value(weight, timeout=5000)

    def hit_next_button(self):
        """Click the 'Next' button."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=10000)
        next_button.click(timeout=10000)
