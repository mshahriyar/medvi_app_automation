# 🏥 MEDVi Automation Testing Project

## 📋 Project Overview

This project automates the **MEDVi qualification flow** using **Playwright + Pytest**, producing **Allure reports** with detailed steps, logs, and screenshots.  
It simulates the complete user journey — from initial qualification to health assessment — and provides client-ready reports ideal for presentations and CI/CD pipelines.

---

## 🎯 What This Project Does

- 🤖 **Automated End-to-End Testing** – Covers the complete MEDVi flow  
- 📊 **Allure Reporting** – Generates interactive visual reports  
- 🖼️ **Screenshots on Failures** – Automatically captured for every failed step  
- 📧 **Client-Ready Reports** – Easy to share and review  
- 🔁 **CI/CD Compatible** – Integrates with GitHub Actions or Jenkins  

---

## 🚀 Quick Start Guide

### 🧩 Prerequisites

- Python **3.8+**  
- macOS / Linux / Windows  
- Chrome browser installed  
- Node.js (optional, for Allure CLI)

---

### 🏗️ 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd medvi_app_automation

# Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps


🧪 2. Run Tests
✅ Option A: Full Allure Test Run
pytest -v -s --alluredir=allure-results --clean-alluredir

📊 3. Generate & View Allure Reports

After test execution, generate and open the report:

# Generate Allure report
allure generate allure-results -o allure-report --clean

# Open the interactive report
allure open allure-report

Directory structure:

medvi_app_automation/
├── tests/
│   └── test_medvi_flow.py               # Main qualification test
├── pages/
│   ├── base_page.py                     # Common helper methods
│   ├── home_page.py
│   ├── height_weight_page.py
│   ├── goal_weight_page.py
│   └── ...                              # All flow pages
├── config/
│   └── config.py                        # App URLs and environment variables
├── reports/                             # Optional legacy HTML reports
├── allure-results/                      # Raw Allure test data
├── allure-report/                       # Generated Allure HTML output
├── screenshots/                         # Failure screenshots
├── conftest.py                          # Fixtures and setup
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Dependencies list
└── README.md                            # This file

|Purpose & Commands             |                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 🧹 Clean & Run Tests | `pytest --alluredir=allure-results --clean-alluredir`                                                                     |
| 📊 Generate Report   | `allure generate allure-results -o allure-report --clean`                                                                 |
| 🌐 Open Report       | `allure open allure-report`                                                                                               |
| 🧩 Run Specific Test | `pytest tests/test_medvi_flow.py::test_medvi_qualification_flow --headed -v --alluredir=allure-results --clean-alluredir` |


🏁 Run Summary:

To execute the full workflow manually:

pytest -v -s --alluredir=allure-results --clean-alluredir
allure generate allure-results -o allure-report --clean
allure serve allure-results
allure open allure-report