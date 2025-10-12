from playwright.sync_api import Page, expect
from utils.helpers import PageValidator
from typing import List, Dict, Union


class BasePage:
    """
    Base page class that provides common functionality for all page objects.
    Includes validation utilities for text and image verification.
    """

    IFRAME_SELECTOR = "iframe[title='1tAZd12DZCus']"

    def __init__(self, page: Page):
        self.page = page
        self.frame = self.page.frame_locator(self.IFRAME_SELECTOR)

        # Initialize validator for iframe-based pages
        self.validator = PageValidator(page, self.frame)

        # Initialize page-specific locators
        self._init_locators()

    def _init_locators(self):
        """Override this method in child classes to define page-specific locators."""
        pass

    # ==================== VALIDATION METHODS ====================

    def verify_text_present(self, text: str, timeout: int = 5000, case_sensitive: bool = False) -> bool:
        """Verify that specific text is present on the page."""
        return self.validator.verify_text_present(text, timeout, case_sensitive)

    def verify_text_contains(self, text: str, timeout: int = 5000) -> bool:
        """Verify that text containing the specified string is present."""
        return self.validator.verify_text_contains(text, timeout)

    def verify_multiple_texts(self, texts: List[str], timeout: int = 5000, all_required: bool = True) -> Dict[str, bool]:
        """Verify multiple texts are present on the page."""
        return self.validator.verify_multiple_texts(texts, timeout, all_required)

    def verify_image_present(self, image_selector: str, timeout: int = 5000) -> bool:
        """Verify that an image is present and visible."""
        return self.validator.verify_image_present(image_selector, timeout)

    def verify_image_by_src(self, src_pattern: str, timeout: int = 5000) -> bool:
        """Verify that an image with specific src pattern is present."""
        return self.validator.verify_image_by_src(src_pattern, timeout)

    def verify_image_by_alt(self, alt_text: str, timeout: int = 5000) -> bool:
        """Verify that an image with specific alt text is present."""
        return self.validator.verify_image_by_alt(alt_text, timeout)

    def verify_multiple_images(self, image_selectors: List[str], timeout: int = 5000, all_required: bool = True) -> Dict[str, bool]:
        """Verify multiple images are present on the page."""
        return self.validator.verify_multiple_images(image_selectors, timeout, all_required)

    def verify_page_elements(self, elements_config: Dict[str, Union[str, List[str]]], timeout: int = 5000) -> Dict[str, bool]:
        """Verify multiple page elements (texts and images) based on configuration."""
        return self.validator.verify_page_elements(elements_config, timeout)

    def get_page_text_content(self) -> str:
        """Get all visible text content from the page."""
        return self.validator.get_page_text_content()

    def get_all_images_info(self) -> List[Dict[str, str]]:
        """Get information about all images on the page."""
        return self.validator.get_all_images_info()

    # ==================== COMMON PAGE METHODS ====================

    def verify_page_loaded(self, expected_texts: List[str] = None, expected_images: List[str] = None) -> bool:
        """
        Verify that the page has loaded correctly by checking for expected elements.

        Args:
            expected_texts: List of texts that should be present on the page
            expected_images: List of image selectors that should be present

        Returns:
            bool: True if page loaded correctly, False otherwise
        """
        try:
            # Wait for iframe to be ready
            self.page.wait_for_selector(self.IFRAME_SELECTOR, state="attached", timeout=30000)

            # Verify expected texts if provided
            if expected_texts:
                text_results = self.verify_multiple_texts(expected_texts, timeout=10000)
                if not all(text_results.values()):
                    return False

            # Verify expected images if provided
            if expected_images:
                image_results = self.verify_multiple_images(expected_images, timeout=10000)
                if not all(image_results.values()):
                    return False

            return True
        except Exception as e:
            print(f"❌ Page load verification failed: {str(e)}")
            return False

    def take_screenshot(self, name: str = None) -> str:
        """
        Take a screenshot of the current page.

        Args:
            name: Optional name for the screenshot file

        Returns:
            str: Path to the screenshot file
        """
        try:
            if not name:
                import datetime
                name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

            screenshot_path = f"screenshots/{name}.png"
            self.page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"❌ Failed to take screenshot: {str(e)}")
            return ""

    def wait_for_element(self, selector: str, timeout: int = 10000, state: str = "visible"):
        """Wait for an element to be in the specified state."""
        try:
            element = self.frame.locator(selector)
            element.wait_for(state=state, timeout=timeout)
            return element
        except Exception as e:
            print(f"❌ Element not found: {selector} - {str(e)}")
            return None

def assert_visible(self, locator, name):
    expect(locator).to_be_visible(timeout=5000)
    self.log.info(f"✅ {name} is visible")
