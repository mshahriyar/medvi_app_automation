# 🏥 MEDVi Automation Testing Project

## 📋 Project Overview

This project contains automated tests for the MEDVi qualification flow, providing comprehensive HTML reports with screenshots for client presentation. The automation covers the complete user journey from initial qualification to final health assessment.

## 🎯 What This Project Does

- **Automated Testing**: Tests the complete MEDVi qualification flow
- **HTML Reporting**: Generates professional, self-contained HTML reports
- **Screenshot Capture**: Automatically captures screenshots on test failures
- **Client-Ready Reports**: Perfect for email sharing and presentations

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- macOS/Linux/Windows
- Chrome browser (for headed mode testing)

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd madvi_automation_project

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps
```

### 2. Run Tests

#### Option A: Simple Test Run
```bash
# Run tests with HTML reporting
pytest tests/test_home.py --headed -v
```

#### Option B: Using HTML Test Runner
```bash
# Run with enhanced HTML reporting
python run_html_tests.py --test tests/test_home.py --headed
```

#### Option C: Using HTML Report Generator
```bash
# Interactive report generator
./html_report_generator.sh
# Choose option 5 for full workflow
```

### 3. View Reports

After running tests, you'll find:

- **HTML Report**: `reports/report.html` - Open in your browser
- **Screenshots**: `screenshots/` - Failure screenshots with timestamps
- **JUnit XML**: `reports/junit.xml` - For CI/CD integration

## 📊 Report Features

### HTML Report Includes:
- ✅ **Test Summary** - Pass/fail statistics and execution time
- ✅ **Detailed Results** - Individual test results with timing
- ✅ **Failure Analysis** - Clear error messages and debugging info
- ✅ **Screenshots** - Visual proof of test execution
- ✅ **Professional Design** - Clean, client-friendly format
- ✅ **Mobile Responsive** - Works on all devices
- ✅ **Self-contained** - Single HTML file, easy to share

### Screenshots Include:
- 📸 **Failure Screenshots** - Full-page captures on test failures
- ⏰ **Timestamped** - When each screenshot was taken
- 🏷️ **Named Files** - Descriptive filenames for easy identification

## 🎯 For Clients

### How to View Reports:

1. **HTML Report (Recommended)**:
   - Open `reports/report.html` in any web browser
   - Perfect for email sharing and presentations
   - Self-contained - no external dependencies

2. **Screenshots**:
   - Browse the `screenshots/` folder
   - Visual verification of test execution
   - Evidence of form filling and navigation

### Report Benefits:
- 📧 **Email Ready** - Attach HTML file to emails
- 📱 **Universal Access** - Works on desktop, tablet, mobile
- 💾 **Offline Viewing** - No internet connection required
- 🔗 **Easy Sharing** - Send single HTML file to stakeholders

## 🧪 Test Coverage

The automation covers the complete MEDVi qualification flow:

1. **Home Page Navigation** - Landing page and qualification button
2. **Height & Weight** - Form filling with validation
3. **Goal Weight** - Target weight setting
4. **Gender & Age** - Demographics collection
5. **Experience Illness** - Health condition assessment
6. **Priority Goals** - User priority selection
7. **Rank Assessment** - User ranking
8. **Metabolic Graph** - Visual data presentation
9. **GLP Information** - Medical information display
10. **Testimonials** - User feedback display
11. **Reasons** - User motivation capture
12. **Weight Loss Expectations** - Timeline setting
13. **Metabolism Analysis** - Health analysis
14. **Sleep Assessment** - Sleep pattern evaluation
15. **Body Review** - Physical assessment
16. **Health Conditions** - Medical history
17. **Additional Questions** - Comprehensive health survey

## 🔧 Configuration

### Test Configuration (`pytest.ini`):
- HTML reporting enabled
- Screenshot capture on failures
- Detailed logging
- Custom test markers

### Test Data:
- Random data generation for realistic testing
- Configurable user profiles
- Comprehensive form validation

## 📁 Project Structure

```
madvi_automation_project/
├── tests/                    # Test files
│   └── test_home.py         # Main test suite
├── pages/                   # Page Object Model
│   ├── base_page.py        # Base page class
│   ├── height_and_weight.py # Height/weight page
│   ├── goal_weight.py      # Goal weight page
│   └── ...                 # Other page objects
├── config/                  # Configuration files
│   ├── config.py           # Test configuration
│   └── validation_config.py # Validation settings
├── utils/                   # Utility functions
│   ├── helpers.py          # Helper functions
│   └── html_reporting.py   # HTML reporting utilities
├── reports/                 # Generated reports
│   ├── report.html         # HTML report
│   └── junit.xml           # JUnit XML
├── screenshots/             # Failure screenshots
├── run_html_tests.py       # HTML test runner
├── html_report_generator.sh # Report generator script
├── pytest.ini              # Test configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Running Tests

### Basic Test Run:
```bash
pytest tests/test_home.py --headed -v
```

### With Specific Browser:
```bash
pytest tests/test_home.py --browser chromium --headed -v
```

### Generate Client Package:
```bash
./html_report_generator.sh
# Choose option 5 for complete workflow
```

## 📈 Understanding Test Results

### Passed Tests:
- ✅ Green checkmark indicates successful test execution
- All form validations completed successfully
- Navigation between pages working correctly

### Failed Tests:
- ❌ Red X indicates test failure
- Screenshots automatically captured
- Detailed error information provided
- Page source included for debugging

### Report Metrics:
- **Execution Time**: How long tests took to run
- **Success Rate**: Percentage of passing tests
- **Failure Analysis**: Detailed breakdown of issues

## 🛠️ Troubleshooting

### Common Issues:

1. **Tests not running**:
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate

   # Check if pytest is installed
   pip install pytest
   ```

2. **Browser not launching**:
   ```bash
   # Install Playwright browsers
   python -m playwright install --with-deps
   ```

3. **Reports not generating**:
   ```bash
   # Check if reports directory exists
   mkdir -p reports screenshots
   ```

4. **Screenshots not capturing**:
   - Ensure `screenshots/` directory exists
   - Check file permissions
   - Verify test failures are occurring

### Getting Help:

- Check the test logs for detailed error messages
- Review screenshots in the `screenshots/` directory
- Examine the HTML report for failure analysis
- Contact the automation team for technical support

## 📞 Support

For questions about:
- **Test Execution**: Check the HTML report for detailed results
- **Technical Issues**: Review screenshots and error logs
- **Report Interpretation**: Contact the automation team
- **Client Presentations**: Use the HTML report for stakeholder meetings

## 🎉 Success Metrics

A successful test run will show:
- ✅ All 17 test steps completed
- 📊 100% form validation success
- 📸 Screenshots captured (if any failures)
- 📄 Professional HTML report generated
- 🎯 Client-ready presentation materials

---

**Ready to test! Run `pytest tests/test_home.py --headed -v` to start your MEDVi automation testing journey.** 🚀
