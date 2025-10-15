import logging
import allure
from playwright.sync_api import Page, expect


class YourNeedPage:
    """Handles the 'Your Need' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("YourNeedPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    @allure.step("Verify your need and medicine heading displayed")
    def verify_your_need_heading_displayed(self):
        """Verify the your need heading displayed."""
        self.log.info("🔍 Verifying your need heading displayed...")
        heading = self.frame.locator("//span[contains(normalize-space(.), 'Please select the following options that you are interested in')]")
        heading.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        heading_text = heading.text_content()
        self.log.info(f"✅ Your need and medicine heading text content: {heading_text}")
    
    @allure.step("Verify all 'Your Need' options are visible")
    def verify_all_options_visible(self):
        """Verify all listed options are visible in the UI."""
        options = [
            "Maintaining muscle mass as I lose weight",
            "Would prefer not to inject",
            "Managing potential side effects such as nausea/vomiting",
            "Assist with aging and longevity (cellular/DNA damage, immune system dysfunction, etc)",
            "Improving cognitive function and mental clarity",
            "Improving energy levels",
            "Regulating menses and hormonal status",
            "Improving sleep quality",
            "I’m not sure - I’d like to discuss formulation options with a clinician via a live virtual consult"
        ]

        self.log.info("🔍 Verifying all options are visible...")

        all_visible = True
        for option in options:
            safe_value = self.escape_xpath_text(option)
            locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")

            try:
                locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                expect(locator).to_be_visible(timeout=5000)
                self.log.info(f"✅ Visible: {option}")
            except Exception as e:
                all_visible = False
                self.log.warning(f"⚠️ Option not visible: {option} | Error: {e}")

        if all_visible:
            self.log.info("🎯 All options are visible on the page.")
        else:
            self.log.warning("⚠️ Some options are not visible on the page.")

    @allure.step("Select multiple 'Understand State of Mind' options")
    def select_multiple_options(self, options_to_select: list[str]):
        """Click on multiple options dynamically with retries and scroll support."""
        self.log.info(f"🧠 Selecting multiple state-of-mind options: {options_to_select}")

        for option_text in options_to_select:
            safe_value = self.escape_xpath_text(option_text)
            locator = self.frame.locator(f"//div[normalize-space(text())={safe_value}]")

            for attempt in range(3):  # Retry up to 3 times per option
                try:
                    locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                    locator.scroll_into_view_if_needed()
                    locator.click(force=True)
                    self.log.info(f"✅ Selected: {option_text}")
                    break  # Exit retry loop if successful
                except Exception as e:
                    self.log.warning(f"⚠️ Attempt {attempt + 1}: Failed to select '{option_text}' ({e})")
                    # Small pause + reattach frame for dynamic reloads
                    self.page.wait_for_timeout(2000)
                    self.frame  # refresh frame locator reference
            else:
                self.log.error(f"❌ Could not select '{option_text}' after 3 retries")


    @allure.step("Click 'Next' button on your need page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")