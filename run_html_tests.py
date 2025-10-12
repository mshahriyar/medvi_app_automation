
import subprocess
import sys
import os
from datetime import datetime
import argparse


class HTMLTestRunner:
    """HTML-focused test runner with comprehensive reporting capabilities."""

    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.reports_dir = os.path.join(self.project_root, "reports")
        self.screenshots_dir = os.path.join(self.project_root, "screenshots")

        # Ensure directories exist
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def run_tests(self, test_path="tests/", browser="chromium", headed=False, parallel=False):
        """
        Run tests with comprehensive HTML reporting.

        Args:
            test_path: Path to test files or specific test
            browser: Browser to use (chromium, firefox, webkit)
            headed: Run browser in headed mode
            parallel: Run tests in parallel
        """
        print("🚀 Starting MEDVi Automation Test Suite (HTML Reporting)")
        print("=" * 60)

        # Build pytest command
        cmd = ["python", "-m", "pytest"]

        # Add test path
        cmd.append(test_path)

        # Add browser option
        if browser:
            cmd.extend(["--browser", browser])

        # Add headed mode
        if headed:
            cmd.append("--headed")

        # Add parallel execution
        if parallel:
            cmd.extend(["-n", "auto"])

        print(f"📋 Command: {' '.join(cmd)}")
        print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        try:
            # Run tests
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=False)

            print()
            print("=" * 60)
            print(f"🕐 End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            if result.returncode == 0:
                print("✅ All tests completed successfully!")
            else:
                print("❌ Some tests failed!")

            return result.returncode

        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return 1

    def generate_html_report(self):
        """Generate HTML report summary."""
        print("\n📄 HTML Report Summary:")

        html_report_path = os.path.join(self.reports_dir, "report.html")
        if os.path.exists(html_report_path):
            file_size = os.path.getsize(html_report_path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"✅ HTML report generated: {html_report_path}")
            print(f"📊 File size: {file_size_mb:.2f} MB")
            print(f"🌐 Open in browser: file://{html_report_path}")
            print(f"📧 Ready for email sharing: Self-contained HTML file")
        else:
            print("❌ HTML report not found")

    def generate_junit_report(self):
        """Generate JUnit XML report summary."""
        print("\n📋 JUnit XML Report Summary:")

        junit_report_path = os.path.join(self.reports_dir, "junit.xml")
        if os.path.exists(junit_report_path):
            print(f"✅ JUnit XML report generated: {junit_report_path}")
        else:
            print("❌ JUnit XML report not found")

    def show_screenshots_summary(self):
        """Show screenshots summary."""
        print("\n📸 Screenshots Summary:")

        if os.path.exists(self.screenshots_dir):
            screenshots = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
            print(f"📊 Total screenshots captured: {len(screenshots)}")

            if screenshots:
                print("📁 Screenshot files:")
                for screenshot in screenshots[:10]:  # Show first 10
                    print(f"   - {screenshot}")
                if len(screenshots) > 10:
                    print(f"   ... and {len(screenshots) - 10} more")
        else:
            print("❌ Screenshots directory not found")

    def create_client_summary(self):
        """Create a comprehensive summary for the client."""
        print("\n📊 CLIENT REPORT SUMMARY")
        print("=" * 60)

        # Test execution summary
        print("🧪 TEST EXECUTION:")
        print(f"   Project: MEDVi Automation")
        print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Reports Directory: {self.reports_dir}")

        # Report files
        print("\n📄 AVAILABLE REPORTS:")

        # HTML report
        html_report_path = os.path.join(self.reports_dir, "report.html")
        if os.path.exists(html_report_path):
            file_size = os.path.getsize(html_report_path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"   ✅ HTML Report: reports/report.html")
            print(f"      - File size: {file_size_mb:.2f} MB")
            print(f"      - Self-contained (single file)")
            print(f"      - Perfect for email sharing")
            print(f"      - Professional format")
            print(f"      - Mobile-friendly responsive design")

        # JUnit XML
        junit_report_path = os.path.join(self.reports_dir, "junit.xml")
        if os.path.exists(junit_report_path):
            print(f"   ✅ JUnit XML: reports/junit.xml")
            print(f"      - CI/CD integration")
            print(f"      - Machine-readable format")

        # Screenshots
        if os.path.exists(self.screenshots_dir):
            screenshots = [f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')]
            print(f"   ✅ Screenshots: {len(screenshots)} files in screenshots/")
            print(f"      - Failure screenshots")
            print(f"      - Step-by-step captures")
            print(f"      - Full page screenshots")

        print("\n🌐 HOW TO VIEW REPORTS:")
        print("   1. HTML Report (Recommended):")
        print(f"      - Open: file://{html_report_path}")
        print("      - Or double-click the file")
        print("   2. Screenshots:")
        print(f"      - Browse: {self.screenshots_dir}/")

        print("\n📈 HTML REPORT FEATURES:")
        print("   ✅ Test execution timeline")
        print("   ✅ Pass/fail statistics")
        print("   ✅ Detailed error analysis")
        print("   ✅ Screenshots on failures")
        print("   ✅ Test data and form inputs")
        print("   ✅ Page source for debugging")
        print("   ✅ Console logs and errors")
        print("   ✅ Performance metrics")
        print("   ✅ Professional design")
        print("   ✅ Mobile responsive")

        print("\n🎯 FOR CLIENTS:")
        print("   📄 HTML Report: Perfect for email sharing and presentations")
        print("   📸 Screenshots: Visual proof of test execution")
        print("   📊 Summary Stats: Quick overview of test results")


def main():
    """Main function to run the test suite."""
    parser = argparse.ArgumentParser(description="MEDVi Automation HTML Test Runner")
    parser.add_argument("--test", default="tests/", help="Test path or specific test file")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"],
                       help="Browser to use")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--summary", action="store_true", help="Show client summary only")

    args = parser.parse_args()

    runner = HTMLTestRunner()

    if args.summary:
        runner.create_client_summary()
        return 0

    # Run tests
    exit_code = runner.run_tests(
        test_path=args.test,
        browser=args.browser,
        headed=args.headed,
        parallel=args.parallel
    )

    # Generate reports
    runner.generate_html_report()
    runner.generate_junit_report()
    runner.show_screenshots_summary()

    # Show client summary
    runner.create_client_summary()

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
