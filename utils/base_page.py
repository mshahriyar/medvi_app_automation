
from playwright.sync_api import Page
import logging
from typing import ClassVar, Optional


class BasePage:
    """Minimal shared base for all MEDVi page objects."""


    IFRAME_SELECTOR: ClassVar[str] = "iframe[title='1tAZd12DZCus']"
    DEFAULT_TIMEOUT: ClassVar[int] = 10_000

    def __init__(self, page: Page):
        self.page = page
        self.log = logging.getLogger(self.__class__.__name__)

    @property
    def frame(self):
        """Always return a fresh frame locator to avoid stale references."""
        return self.page.frame_locator(self.IFRAME_SELECTOR)

    @staticmethod
    def escape_xpath_text(text: str) -> str:
        """Safely escape text for XPath literal (handles both ' and ")."""
        if "'" not in text:
            return f"'{text}'"
        if '"' not in text:
            return f'"{text}"'
        parts = text.split("'")
        return "concat(" + ", \"'\", ".join(f"'{p}'" for p in parts) + ")"
