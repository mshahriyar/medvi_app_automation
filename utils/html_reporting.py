
import os
from datetime import datetime
from playwright.sync_api import Page
from typing import Optional, Dict, Any


class HTMLReportManager:
    """Manages comprehensive HTML test reporting with screenshots and detailed analysis."""

    def __init__(self, page: Page):
        self.page = page
        self.test_start_time = datetime.now()
        self.screenshots_dir = "screenshots"
        self.reports_dir = "reports"

        # Ensure directories exist
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

    def capture_step_screenshot(self, step_name: str, description: str = "") -> str:
        """
        Capture a screenshot for a specific test step.

        Args:
            step_name: Name of the test step
            description: Optional description of what's happening

        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{step_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshots_dir, filename)

        try:
            self.page.screenshot(path=screenshot_path, full_page=True)

            if description:
                print(f"📸 Screenshot captured: {screenshot_path} - {description}")
            else:
                print(f"📸 Screenshot captured: {screenshot_path}")

            return screenshot_path

        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")
            return ""

    def capture_page_info(self, step_name: str):
        """
        Capture comprehensive page information for debugging.

        Args:
            step_name: Name of the current step
        """
        try:
            # Capture current URL
            current_url = self.page.url
            print(f"🔗 {step_name} - Current URL: {current_url}")

            # Capture page title
            page_title = self.page.title()
            print(f"📄 {step_name} - Page Title: {page_title}")

            # Capture console logs if available
            try:
                logs = self.page.evaluate("() => { return window.console.logs || []; }")
                if logs:
                    print(f"🐛 {step_name} - Console Logs: {logs}")
            except:
                pass

        except Exception as e:
            print(f"❌ Failed to capture page info: {e}")

    def log_step_completion(self, step_name: str, success: bool = True, details: str = ""):
        """
        Log step completion with appropriate output.

        Args:
            step_name: Name of the completed step
            success: Whether the step was successful
            details: Additional details about the step
        """
        status = "✅ PASSED" if success else "❌ FAILED"
        message = f"{status} - {step_name}"

        if details:
            message += f" - {details}"

        print(message)

    def create_test_summary(self, test_data: Dict[str, Any]):
        """
        Create a comprehensive test summary for the client.

        Args:
            test_data: Complete test data used in the test
        """
        try:
            summary = f"""
TEST EXECUTION SUMMARY
=====================
Test Start Time: {self.test_start_time.strftime('%Y-%m-%d %H:%M:%S')}
Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test Duration: {datetime.now() - self.test_start_time}

TEST DATA USED:
===============
"""
            for key, value in test_data.items():
                summary += f"{key}: {value}\n"

            summary += f"""
SCREENSHOTS CAPTURED:
====================
Screenshots saved in: {self.screenshots_dir}/
Total screenshots: {len([f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')])}

REPORTS GENERATED:
=================
- HTML Report: reports/report.html
- JUnit XML: reports/junit.xml
"""

            print(summary)
            print("📊 Test summary created")

        except Exception as e:
            print(f"❌ Failed to create test summary: {e}")


def enhance_test_with_html_reporting(test_func):
    """
    Decorator to automatically enhance any test function with comprehensive HTML reporting.

    Usage:
        @enhance_test_with_html_reporting
        def test_my_feature(page, user_data):
            # Your test code here
            pass
    """
    def wrapper(*args, **kwargs):
        # Find the page object in the arguments
        page = None
        for arg in args:
            if hasattr(arg, 'screenshot'):  # Check if it's a Playwright page
                page = arg
                break

        if page:
            report_manager = HTMLReportManager(page)

            # Add report manager to kwargs for use in test
            kwargs['report_manager'] = report_manager

            # Execute the test
            result = test_func(*args, **kwargs)

            # Create final summary
            if 'user_data' in kwargs:
                report_manager.create_test_summary(kwargs['user_data'])

            return result
        else:
            return test_func(*args, **kwargs)

    return wrapper


# Utility functions for common HTML reporting tasks
def log_form_data(form_data: Dict[str, Any], step_name: str):
    """Log form data for HTML report."""
    try:
        print(f"📋 {step_name} - Form Data:")
        for key, value in form_data.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"❌ Failed to log form data: {e}")


def log_validation_result(validation_name: str, passed: bool, details: str = ""):
    """Log validation result for HTML report."""
    status = "✅ PASSED" if passed else "❌ FAILED"
    message = f"{validation_name}: {status}"

    if details:
        message += f" - {details}"

    print(message)


def log_error_analysis(error_message: str, context: str = ""):
    """Log detailed error analysis for HTML report."""
    analysis = f"""
ERROR ANALYSIS
=============
Error: {error_message}
Context: {context}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

POSSIBLE CAUSES:
- Element not found or not visible
- Page not fully loaded
- Network connectivity issues
- Application state changes
- Timing issues with dynamic content

RECOMMENDED ACTIONS:
- Check element selectors
- Add explicit waits
- Verify page state
- Review application logs
"""

    print(analysis)
