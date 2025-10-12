
import logging
import os
import random as rnd
import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL
from datetime import datetime
from pages.experience_illness import ExperienceIllnessPage
from pages.gender_and_age import GenderAndAgePage
from pages.height_and_weight import AddHeightAndWeight
from pages.goal_weight import GoalWeightPage
from pages.priority import PriorityPage
import csv
from datetime import datetime
from pages.metabolic_graph import MetabolicGraphPage
from pages.glp import GPL1Page
from pages.rank import RankPage
from pages.frank_new_man import FrankNewManPage
from pages.reasons import ReasonsPage
from pages.lose_weight import LoseWeightPage
from pages.analyze_metabolism import AnalyzeMetabolismPage
from pages.sleep_check import SleepCheckPage
from pages.sleep_hours import SleepHoursPage
from pages.body_review import BodyReviewPage
from pages.health_conditions import HealthConditionsPage
from pages.additional_health_questions import AdditionalHealthQuestionsPage
# --------------------- Logging Configuration --------------------- #

@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    """Set up root logging for all tests."""
    level_name = os.getenv("LOG_LEVEL", "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(asctime)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger()
    logger.info("✅ Logging configured.")
    yield


# ------------------- HTML Reporting Hooks ------------------- #

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Enhanced reporting hook that captures screenshots on test failures.
    Provides comprehensive failure analysis for HTML reports.
    """
    outcome = yield
    rep = outcome.get_result()

    # Only capture on failures during the call phase
    if rep.when == "call" and rep.failed:
        # Get the page object if available
        page = None
        if hasattr(item, 'funcargs'):
            page = item.funcargs.get('page')

        if page:
            try:
                # Generate timestamp for unique filenames
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name.replace(" ", "_").replace("::", "_")

                # Create failure screenshot
                screenshot_path = f"screenshots/failure_{test_name}_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)

                print(f"📸 Failure screenshot saved: {screenshot_path}")

            except Exception as e:
                print(f"❌ Failed to capture failure details: {e}")


# ------------------- Playwright Fixtures ------------------- #

@pytest.fixture(scope="session")
def playwright():
    """Playwright instance for the test session."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright, request):
    """Browser instance for the test session with smart headless/headed detection."""

    # Check if --headed flag is passed
    is_headed = request.config.getoption("--headed", default=False)

    if is_headed:
        print("🚀 Launching browser in headed mode (--headed flag detected)...")
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security'
            ]
        )
        print("✅ Browser launched successfully in headed mode")
    else:
        print("🚀 Launching browser in headless mode for better performance...")
        try:
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection'
                ]
            )
            print("✅ Browser launched successfully in headless mode")
        except Exception as e:
            print(f"⚠️ Headless mode failed: {e}")
            print("🔄 Falling back to headed mode...")
            browser = playwright.chromium.launch(
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security'
                ]
            )
            print("✅ Browser launched successfully in headed mode")

    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_init_script("localStorage.clear(); sessionStorage.clear();")
    page = context.new_page()
    yield page
    context.close()
    browser.close()

# ------------------- Base URL Fixture ------------------- #

@pytest.fixture(scope="session")
def base_url():
    """Return the application's base URL."""
    return BASE_URL


# ------------------- Page Object Fixtures ------------------- #

@pytest.fixture
def add_height_weight(page):
    """Return an instance of the AddHeightAndWeight page."""
    return AddHeightAndWeight(page)

@pytest.fixture
def goal_weight(page):
    """Return an instance of the GoalWeight page."""
    return GoalWeightPage(page)

@pytest.fixture
def gender_and_age(page):
    """Fixture returning an instance of the GenderAndAgePage."""
    return GenderAndAgePage(page)

@pytest.fixture
def experience_illness(page):
    """Fixture returning an instance of the ExperienceIllnessPage."""
    return ExperienceIllnessPage(page)

@pytest.fixture
def priority(page):
    """Fixture returning an instance of the PriorityPage."""
    return PriorityPage(page)

@pytest.fixture
def rank(page):
    """Fixture returning an instance of the RankPage."""
    return RankPage(page)

@pytest.fixture
def metabolic_graph(page):
    """Fixture returning an instance of the MetabolicGraphPage."""
    return MetabolicGraphPage(page)

@pytest.fixture
def frank_new_man(page):
    """Fixture returning an instance of the FrankNewManPage."""
    return FrankNewManPage(page)

@pytest.fixture
def gpl(page):
    """Fixture returning an instance of the GPL1Page."""
    return GPL1Page(page)

@pytest.fixture
def reasons(page):
    """Fixture returning an instance of the ReasonsPage."""
    return ReasonsPage(page)

@pytest.fixture
def lose_weight(page):
    """Fixture returning an instance of the LoseWeightPage."""
    return LoseWeightPage(page)

@pytest.fixture
def analyze_metabolism(page):
    """Fixture returning an instance of the AnalyzeMetabolismPage."""
    return AnalyzeMetabolismPage(page)

@pytest.fixture
def sleep_check(page):
    """Fixture returning an instance of the SleepCheckPage."""
    return SleepCheckPage(page)

@pytest.fixture
def sleep_hours(page):
    """Fixture returning an instance of the SleepHoursPage."""
    return SleepHoursPage(page)

@pytest.fixture
def body_review(page):
    """Fixture returning an instance of the BodyReviewPage."""
    return BodyReviewPage(page)

@pytest.fixture
def health_conditions(page):
    """Fixture returning an instance of the HealthConditionsPage."""
    return HealthConditionsPage(page)

@pytest.fixture
def additional_health_questions(page):
    """Fixture returning an instance of the AdditionalHealthQuestionsPage."""
    return AdditionalHealthQuestionsPage(page)

# ------------------- Data Fixture (Dynamic) ------------------- #

@pytest.fixture
def user_data():
    """
    Generate realistic, random user data for each run.
    This keeps every test execution unique.
    """
    logger = logging.getLogger("user_data")

    # Height / Weight
    feet = str(rnd.choice(range(4, 7)))          # 4–6 ft
    inches = str(rnd.choice(range(0, 12)))       # 0–11 in
    weight = rnd.randint(100, 300)               # 100–300 lbs

    # Ensure goal weight is always less than current weight but not below 90
    lower_bound = 90
    upper_bound = max(91, weight - 20)  # prevent invalid upper range

    goal_weight = rnd.randint(lower_bound, upper_bound)


    # Demographics
    gender = rnd.choice(["Male"])
    experience_illness = rnd.choice(["Hair Loss", "Skin Issues", "Cognition Issues", "None of these"])
    priority = rnd.choice(["Lose Weight", "Gain Muscle", "Maintain My Current Body"])
    age_range = rnd.choice(["18-28", "29-39", "40-50", "51-61", "62+"])
    reason_for_weight_loss = rnd.choice(["I want to live longer", "I want to feel and look better", "I want to reduce current health issues", "All of these"])
    lose_weight_goal = rnd.choice(["That works for me", "I want it faster", "That's too fast"])
    sleep_routine = rnd.choice(["Pretty Good", "A bit restless", "I don't sleep well"])
    sleep_hours = rnd.choice(["Less than 5 hours", "6-7 hours", "8-9 hours", "More than 9 hours"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "timestamp": timestamp,
        "feet": feet,
        "inches": inches,
        "weight": str(weight),
        "goal_weight": str(goal_weight),
        "gender": gender,
        "age": age_range,
        "experience_illness": experience_illness,
        "priority": priority,
        "reason": reason_for_weight_loss,
        "lose_weight": lose_weight_goal,
        "sleep": sleep_routine,
        "sleep_hours": sleep_hours,
    }

    logger.info(f"🧮 Generated Test Data → {data}")

    # Save (append) to CSV file
    os.makedirs("logs", exist_ok=True)
    csv_file = f"logs/random_data_log_{datetime.now().strftime('%Y-%m-%d')}.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()  # only once
        writer.writerow(data)

    return data


