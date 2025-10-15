import logging
import allure
from playwright.sync_api import Page, expect


class InfoSharedWithMedicalTeamPage:
    """Handles the 'Info Shared With Medical Team' step in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("InfoSharedWithMedicalTeamPage")

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)
        
    @allure.step("Verify info shared with medical team heading displayed")
    def verify_info_shared_with_medical_team_heading_displayed(self):
        """Verify the info shared with medical team heading displayed."""
        self.log.info("🔍 Verifying info shared with medical team heading displayed...")
        heading = self.frame.locator("//span[text() ='Do you have any further information which you would like our medical team to know?']")
        expect(heading).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Info shared with medical team heading displayed verified successfully")

    @allure.step("Select currently taking medicine option")
    def select_info_shared_with_medical_team_option(self, option: str):
        """Select the currently taking medicine option."""
        self.log.info(f"💊 Selecting currently taking medicine option: {option}")
        option_locator = self.frame.locator(f"//div[normalize-space(text())='{option}']")
        option_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        option_locator.scroll_into_view_if_needed()
        option_locator.click()
        if option == "Yes":
            provide_info_text = self.frame.locator("//span[text() ='Provide details here. Please do not include urgent or emergency medical information.']")
            expect(provide_info_text).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
            self.log.info("✅ Provide info text displayed verified successfully")
            info_shared_with_medical_team_input = self.frame.locator("//textarea[@data-cy= 'text-area']")
            info_shared_with_medical_team_input.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            info_shared_with_medical_team_input.fill("hiiiiiiii how are you? what you tooks")
            self.log.info(f"✅ Entered info shared with medical team: hiiiiiii how are you? what you tooks")
            
        self.log.info(f"✅ Selected info shared with medical team option: {option}")

    @allure.step("Click 'Next' button on info shared with medical team page")
    def hit_next_button(self):
        """Click the 'Next' button to continue."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")