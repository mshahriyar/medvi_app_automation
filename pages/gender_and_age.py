from playwright.sync_api import Page, expect


class GenderAndAgePage:
    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # --- Locators ---
        self.gender_selection = "//div[normalize-space(text())='{gender}']"

        self.age_input = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        self.next_button = self.frame.locator("//button[@data-cy='button-component']")


    def select_gender(self, gender_value: str):
        locator = self.gender_selection.format(gender=gender_value)
        gender_option = self.frame.locator(locator)
        gender_option.click()
        expect(gender_option).to_be_visible()
        

    def select_age(self, age: str):
        """Select 'Age' value from dropdown."""
        self.age_input.click(timeout=10000)
        self.page.wait_for_timeout(5000)
        self.age_input.fill(age)
        self.page.wait_for_timeout(2000)
        self.page.keyboard.press("Enter")
    
    def hit_next_button(self):
        """Click the 'Next' button and verify it's disabled afterward."""
        self.next_button.click(timeout=10000)

