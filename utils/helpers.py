from playwright.sync_api import expect, Locator, Page
from typing import List, Dict, Union, Optional
import logging

logger = logging.getLogger(__name__)

def verify_element_visible(element):
    """Utility to verify an element is visible."""
    expect(element).to_be_visible(timeout=5000)


class PageValidator:
    """
    Generic validation utility for text and image verification across all pages.
    Can be used with any page object that has a frame locator.
    """

    def __init__(self, page: Page, frame_locator=None):
        """
        Initialize the validator.

        Args:
            page: Playwright page object
            frame_locator: Frame locator for iframe-based pages (optional)
        """
        self.page = page
        self.frame_locator = frame_locator
        self.base_locator = frame_locator if frame_locator else page

    def verify_text_present(self, text: str, timeout: int = 5000, case_sensitive: bool = False) -> bool:
        """
        Verify that specific text is present on the page.

        Args:
            text: Text to search for
            timeout: Timeout in milliseconds
            case_sensitive: Whether the search should be case sensitive

        Returns:
            bool: True if text is found, False otherwise
        """
        try:
            if case_sensitive:
                locator = self.base_locator.locator(f"text='{text}'")
            else:
                locator = self.base_locator.locator(f"text='{text}'").or_(self.base_locator.locator(f"text='{text.lower()}'")).or_(self.base_locator.locator(f"text='{text.upper()}'"))

            locator.wait_for(state="visible", timeout=timeout)
            logger.info(f"✅ Text found: '{text}'")
            return True
        except Exception as e:
            logger.warning(f"❌ Text not found: '{text}' - {str(e)}")
            return False

    def verify_text_contains(self, text: str, timeout: int = 5000) -> bool:
        """
        Verify that text containing the specified string is present.

        Args:
            text: Partial text to search for
            timeout: Timeout in milliseconds

        Returns:
            bool: True if text is found, False otherwise
        """
        try:
            locator = self.base_locator.locator(f"text*='{text}'")
            locator.wait_for(state="visible", timeout=timeout)
            logger.info(f"✅ Text containing '{text}' found")
            return True
        except Exception as e:
            logger.warning(f"❌ Text containing '{text}' not found - {str(e)}")
            return False

    def verify_multiple_texts(self, texts: List[str], timeout: int = 5000, all_required: bool = True) -> Dict[str, bool]:
        """
        Verify multiple texts are present on the page.

        Args:
            texts: List of texts to verify
            timeout: Timeout in milliseconds
            all_required: If True, all texts must be present. If False, at least one must be present.

        Returns:
            Dict[str, bool]: Dictionary with text as key and found status as value
        """
        results = {}
        for text in texts:
            results[text] = self.verify_text_present(text, timeout)

        if all_required:
            all_found = all(results.values())
            logger.info(f"📋 All texts verification: {'✅ PASSED' if all_found else '❌ FAILED'}")
        else:
            any_found = any(results.values())
            logger.info(f"📋 Any text verification: {'✅ PASSED' if any_found else '❌ FAILED'}")

        return results

    def verify_image_present(self, image_selector: str, timeout: int = 5000) -> bool:
        """
        Verify that an image is present and visible.

        Args:
            image_selector: CSS selector or XPath for the image
            timeout: Timeout in milliseconds

        Returns:
            bool: True if image is found and visible, False otherwise
        """
        try:
            if image_selector.startswith('//'):
                locator = self.base_locator.locator(image_selector)
            elif image_selector.startswith('img'):
                locator = self.base_locator.locator(image_selector)
            else:
                locator = self.base_locator.locator(f"img{image_selector}")

            locator.wait_for(state="visible", timeout=timeout)
            logger.info(f"✅ Image found: {image_selector}")
            return True
        except Exception as e:
            logger.warning(f"❌ Image not found: {image_selector} - {str(e)}")
            return False

    def verify_image_by_src(self, src_pattern: str, timeout: int = 5000) -> bool:
        """
        Verify that an image with specific src pattern is present.

        Args:
            src_pattern: Pattern to match in image src attribute
            timeout: Timeout in milliseconds

        Returns:
            bool: True if image is found, False otherwise
        """
        try:
            locator = self.base_locator.locator(f"img[src*='{src_pattern}']")
            locator.wait_for(state="visible", timeout=timeout)
            logger.info(f"✅ Image with src pattern '{src_pattern}' found")
            return True
        except Exception as e:
            logger.warning(f"❌ Image with src pattern '{src_pattern}' not found - {str(e)}")
            return False

    def verify_image_by_alt(self, alt_text: str, timeout: int = 5000) -> bool:
        """
        Verify that an image with specific alt text is present.

        Args:
            alt_text: Alt text to search for
            timeout: Timeout in milliseconds

        Returns:
            bool: True if image is found, False otherwise
        """
        try:
            locator = self.base_locator.locator(f"img[alt='{alt_text}']")
            locator.wait_for(state="visible", timeout=timeout)
            logger.info(f"✅ Image with alt text '{alt_text}' found")
            return True
        except Exception as e:
            logger.warning(f"❌ Image with alt text '{alt_text}' not found - {str(e)}")
            return False

    def verify_multiple_images(self, image_selectors: List[str], timeout: int = 5000, all_required: bool = True) -> Dict[str, bool]:
        """
        Verify multiple images are present on the page.

        Args:
            image_selectors: List of image selectors to verify
            timeout: Timeout in milliseconds
            all_required: If True, all images must be present. If False, at least one must be present.

        Returns:
            Dict[str, bool]: Dictionary with selector as key and found status as value
        """
        results = {}
        for selector in image_selectors:
            results[selector] = self.verify_image_present(selector, timeout)

        if all_required:
            all_found = all(results.values())
            logger.info(f"🖼️ All images verification: {'✅ PASSED' if all_found else '❌ FAILED'}")
        else:
            any_found = any(results.values())
            logger.info(f"🖼️ Any image verification: {'✅ PASSED' if any_found else '❌ FAILED'}")

        return results

    def verify_page_elements(self, elements_config: Dict[str, Union[str, List[str]]], timeout: int = 5000) -> Dict[str, bool]:
        """
        Verify multiple page elements (texts and images) based on configuration.

        Args:
            elements_config: Dictionary with element types as keys and selectors/texts as values
                Example: {
                    'texts': ['Welcome', 'Sign Up'],
                    'images': ['img.logo', 'img.banner'],
                    'images_by_src': ['logo.png', 'banner.jpg'],
                    'images_by_alt': ['Company Logo', 'Hero Banner']
                }
            timeout: Timeout in milliseconds

        Returns:
            Dict[str, bool]: Dictionary with element as key and found status as value
        """
        results = {}

        # Verify texts
        if 'texts' in elements_config:
            for text in elements_config['texts']:
                results[f"text: {text}"] = self.verify_text_present(text, timeout)

        # Verify images by selector
        if 'images' in elements_config:
            for selector in elements_config['images']:
                results[f"image: {selector}"] = self.verify_image_present(selector, timeout)

        # Verify images by src pattern
        if 'images_by_src' in elements_config:
            for src_pattern in elements_config['images_by_src']:
                results[f"image_src: {src_pattern}"] = self.verify_image_by_src(src_pattern, timeout)

        # Verify images by alt text
        if 'images_by_alt' in elements_config:
            for alt_text in elements_config['images_by_alt']:
                results[f"image_alt: {alt_text}"] = self.verify_image_by_alt(alt_text, timeout)

        # Summary
        total_elements = len(results)
        found_elements = sum(results.values())
        logger.info(f"📊 Page elements verification: {found_elements}/{total_elements} elements found")

        return results

    def get_page_text_content(self) -> str:
        """
        Get all visible text content from the page.

        Returns:
            str: All visible text content
        """
        try:
            text_content = self.base_locator.locator("body").text_content()
            logger.info("📄 Page text content retrieved")
            return text_content or ""
        except Exception as e:
            logger.warning(f"❌ Failed to get page text content: {str(e)}")
            return ""

    def get_all_images_info(self) -> List[Dict[str, str]]:
        """
        Get information about all images on the page.

        Returns:
            List[Dict[str, str]]: List of dictionaries with image information
        """
        try:
            images = self.base_locator.locator("img").all()
            image_info = []

            for img in images:
                try:
                    info = {
                        'src': img.get_attribute('src') or '',
                        'alt': img.get_attribute('alt') or '',
                        'title': img.get_attribute('title') or '',
                        'visible': img.is_visible()
                    }
                    image_info.append(info)
                except:
                    continue

            logger.info(f"🖼️ Found {len(image_info)} images on page")
            return image_info
        except Exception as e:
            logger.warning(f"❌ Failed to get images info: {str(e)}")
            return []
