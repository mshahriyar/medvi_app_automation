from playwright.sync_api import expect

def verify_element_visible(element):
    """Utility to verify an element is visible."""
    expect(element).to_be_visible(timeout=5000)