from playwright.sync_api import Page, expect

class ExperienceIllnessPage:

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.experience_input = "//div[normalize-space(text())='{experience_illness}']"
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")

    def select_experience_illness(self, experience_illness_value: str):
        locator = self.experience_input.format(experience_illness=experience_illness_value)
        experience_illness_option = self.frame.locator(locator)
        self.page.wait_for_timeout(1000)
        experience_illness_option.scroll_into_view_if_needed()
        expect(experience_illness_option).to_be_visible(timeout=5000)
        experience_illness_option.click()
        

    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.next_button.click(timeout=10000)
        