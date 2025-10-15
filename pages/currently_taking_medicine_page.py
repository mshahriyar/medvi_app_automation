import logging
import allure
from playwright.sync_api import Page, expect


class CurrentlyTakingMedicinePage:
    """Handles the 'Currently Taking Medicine' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("CurrentlyTakingMedicinePage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
        
    @allure.step("Verify currently taking medicine heading and image displayed")
    def verify_currently_taking_medicine_heading_and_image_displayed(self):
        """Verify the currently taking medicine heading and image displayed."""
        self.log.info("🔍 Verifying currently taking medicine heading and image displayed...")
        heading = self.frame.locator("//span[text() ='Do you currently take any medications?']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Currently taking medicine heading verified successfully")
        image = self.frame.locator("img[src*= 'd2cb1908ecae_3.png']")
        expect(image).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Currently taking medicine image displayed verified successfully")

    @allure.step("Select currently taking medicine option")
    def select_currently_taking_medicine_option(self, option: str):
        """Select the currently taking medicine option."""
        self.log.info(f"💊 Selecting currently taking medicine option: {option}")
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        if option == "Yes":
            medicine_input = self.frame.locator("//textarea[@data-cy= 'text-area']")
            medicine_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            medicine_input.fill("Shery mecicine tooks")
            self.log.info(f"✅ Entered medicine name: Shery mecicine tooks")
            
        self.log.info(f"✅ Selected currently taking medicine option: {option}")

    @allure.step("Click 'Next' button on currently taking medicine page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")