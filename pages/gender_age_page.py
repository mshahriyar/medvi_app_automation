from playwright.sync_api import Page, expect
import logging
import allure


class GenderAndAgePage:
    """Handles gender and age selection interactions in the MEDVi Typeform flow."""

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT = 10000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger("GenderAndAgePage")

    @property
    def frame(self):
        """Always fetch a fresh frame locator to avoid stale reference."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    # ---------------------- Actions ---------------------- #

    @allure.step("Select gender")
    def select_gender(self, gender: str):
        """Select Male or Female dynamically."""
        self.log.info(f"👤 Selecting gender: {gender}")
        gender_locator = self.frame.locator(f"//div[normalize-space(text())='{gender}']")
        gender_locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        gender_locator.click()
        self.log.info(f"✅ Selected gender: {gender}")

    @allure.step("Select age range")
    def select_age(self, age: str):
        """Select user's age range from dropdown."""
        self.log.info(f"🎂 Selecting age range: {age}")
        dropdown = self.frame.locator("(//div[@data-cy='dropdown-component'])[1]//input")
        dropdown.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        dropdown.click()
        self.page.wait_for_timeout(500)

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
                self.log.info(f"✅ Selected age range: {term}")
                found = True
                break

        if not found:
            msg = f"❌ Age option '{age}' not found in dropdown"
            self.log.error(msg)
            raise RuntimeError(msg)

    @allure.step("Click 'Next' button")
    def hit_next_button(self):
        """Click the 'Next' button to proceed."""
        next_button = self.frame.locator("//button[@data-cy='button-component']")
        next_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        next_button.click()
        self.log.info("➡️ Clicked 'Next' button")
