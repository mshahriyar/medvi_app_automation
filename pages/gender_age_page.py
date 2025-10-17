from playwright.sync_api import Page, expect
import logging, time
import allure
# pyright: ignore[reportMissingImports]
from utils.base_page import BasePage


class GenderAndAgePage(BasePage):
    """Handles gender and age selection interactions in the MEDVi Typeform flow."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ----------------------- Helpers -----------------------

    def _retry_action(self, func, retries=3, delay=2):
        """Retry a flaky action several times before giving up."""
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

    # ---------------------- Actions ---------------------- #
    @allure.step("Verify gender and age content is visible")
    def verify_gender_and_age_content_visible(self):
        """Verify the gender and age content is visible."""
        self.log.info("🔍 Verifying gender and age content is visible...")
        content = self.frame.locator("//span[text() ='Medication can be tailored to ']")
        option_1 = self.frame.locator("//span[normalize-space(text())='Are you male or female?']")
        option_2 = self.frame.locator("//span[normalize-space(text())='What is your age range?']")
        expect(content).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(option_1).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(option_2).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        self.log.info("✅ Gender and age content is visible verified successfully")

    @allure.step("Select gender")
    def select_gender(self, gender: str):
        """Select Male or Female dynamically."""
        self._retry_action(lambda: self._select_gender(gender))
        self.log.info(f"✅ Selected gender: {gender}")

    @allure.step("Select age range")
    def select_age(self, age: str):
        """Select user's age range from dropdown."""
        self._retry_action(lambda: self._select_age(age))
        self.log.info(f"✅ Selected age range: {age}")

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button safely."""
        self._retry_action(self._click_next)
        self.log.info("➡️ Clicked 'Next' button")

    # ----------------------- Internal Methods -----------------------

    def _select_gender(self, gender: str):
        self.log.info(f"👤 Selecting gender: {gender}")
        gender_locator = self.frame.locator(f"//div[normalize-space(text())='{gender}']")
        gender_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        gender_locator.scroll_into_view_if_needed()
        gender_locator.click()

    def _select_age(self, age: str):
        self.log.info(f"🎂 Selecting age range: {age}")
        dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        dropdown.scroll_into_view_if_needed()
        dropdown.click(force=True)
        listbox = self.frame.locator("//div[@role = 'listbox']")
        listbox.scroll_into_view_if_needed()
        expect(listbox).to_be_visible(timeout=5000)

        # Common text patterns that might appear in the dropdown
        search_terms = [age]
        if "–" in age:
            search_terms.append(age.split("–")[0])
        elif "-" in age:
            search_terms.append(age.split("-")[0])

        found = False
        for term in search_terms:
            option = self.frame.locator(f"//div[contains(text(), '{term}')]")
            if option.count() > 0:
                option.first.click()
                found = True
                break

        if not found:
            msg = f"❌ Age option '{age}' not found in dropdown"
            self.log.error(msg)
            raise RuntimeError(msg)

    def _click_next(self):
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
