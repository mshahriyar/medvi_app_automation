import logging
import os
import random as rnd
import pytest
from playwright.sync_api import sync_playwright
from config.config import BASE_URL
from datetime import datetime
from pages.home_page import HomePage
from pages.height_weight_page import HeightWeightPage
from pages.goal_weight_page import GoalWeightPage
from pages.gender_age_page import GenderAndAgePage
from pages.experience_illness_page import ExperienceIllnessPage
from pages.priority_page import PriorityPage
from pages.rank_page import RankPage
from pages.metabolic_graph_page import MetabolicGraphPage
from pages.glp1_page import GLP1Page
from pages.frank_new_man_page import FrankNewManPage
from pages.reasons_page import ReasonsPage
from pages.lose_weight_page import LoseWeightPage
from pages.analyze_metabolism_page import AnalyzeMetabolismPage
from pages.sleep_check_page import SleepCheckPage
from pages.sleep_hours_page import SleepHoursPage
from pages.body_review_page import BodyReviewPage
from pages.health_conditions_page import HealthConditionsPage
from pages.additional_health_questions_page import AdditionalHealthQuestionsPage
from pages.taken_medication_page import TakenMedicationPage
from pages.glp1_medicine_page import GLP1MedicinePage
from pages.last_three_month_medication_page import lastThreeMonthMedicationPage
from pages.surgery_weight_loss_page import SurgeryWeightLossPage
from pages.weight_loss_program_page import WeightLossProgramPage
from pages.clinically_appropriate_page import ClinicallyAppropriatePage
from pages.weight_change_last_year_page import WeightChangeLastYearPage
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


@pytest.fixture(scope="function")
def browser(playwright, request):
    """Browser instance for each test."""
    browser_type = request.config.getoption("--browser", default="chromium")

    # Handle case where browser_type might be a list
    if isinstance(browser_type, list):
        browser_type = browser_type[0] if browser_type else "chromium"

    headless = not request.config.getoption("--headed", default=False)

    if browser_type == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Page instance for each test."""
    page = browser.new_page()
    yield page
    page.close()


# ------------------- Page Object Fixtures ------------------- #

@pytest.fixture(scope="function")
def home_page(page):
    """Home page fixture."""
    return HomePage(page)


@pytest.fixture(scope="function")
def height_weight_page(page):
    """Height and weight page fixture."""
    return HeightWeightPage(page)


@pytest.fixture(scope="function")
def goal_weight(page):
    """Goal weight page fixture."""
    return GoalWeightPage(page)


@pytest.fixture(scope="function")
def gender_and_age(page):
    """Gender and age page fixture."""
    return GenderAndAgePage(page)


@pytest.fixture(scope="function")
def experience_illness(page):
    """Experience illness page fixture."""
    return ExperienceIllnessPage(page)


@pytest.fixture(scope="function")
def priority(page):
    """Priority page fixture."""
    return PriorityPage(page)


@pytest.fixture(scope="function")
def rank(page):
    """Rank page fixture."""
    return RankPage(page)


@pytest.fixture(scope="function")
def metabolic_graph(page):
    """Metabolic graph page fixture."""
    return MetabolicGraphPage(page)


@pytest.fixture(scope="function")
def gpl(page):
    """GLP-1 page fixture."""
    return GLP1Page(page)


@pytest.fixture(scope="function")
def frank_new_man(page):
    """Frank new man page fixture."""
    return FrankNewManPage(page)


@pytest.fixture(scope="function")
def reasons(page):
    """Reasons page fixture."""
    return ReasonsPage(page)


@pytest.fixture(scope="function")
def lose_weight(page):
    """Lose weight page fixture."""
    return LoseWeightPage(page)


@pytest.fixture(scope="function")
def analyze_metabolism(page):
    """Analyze metabolism page fixture."""
    return AnalyzeMetabolismPage(page)


@pytest.fixture(scope="function")
def sleep_check(page):
    """Sleep check page fixture."""
    return SleepCheckPage(page)


@pytest.fixture(scope="function")
def sleep_hours(page):
    """Sleep hours page fixture."""
    return SleepHoursPage(page)


@pytest.fixture(scope="function")
def body_review(page):
    """Body review page fixture."""
    return BodyReviewPage(page)


@pytest.fixture(scope="function")
def health_conditions(page):
    """Health conditions page fixture."""
    return HealthConditionsPage(page)


@pytest.fixture(scope="function")
def additional_health_questions(page):
    """Additional health questions page fixture."""
    return AdditionalHealthQuestionsPage(page)


@pytest.fixture(scope="function")
def taken_medication(page):
    """Taken medication page fixture."""
    return TakenMedicationPage(page)


@pytest.fixture(scope="function")
def glp1_medicine(page):
    """GLP-1 medicine page fixture."""
    return GLP1MedicinePage(page)


@pytest.fixture(scope="function")
def last_three_month_medication(page):
    """Last three month medication page fixture."""
    return lastThreeMonthMedicationPage(page)


@pytest.fixture(scope="function")
def surgery_weight_loss(page):
    """Surgery weight loss page fixture."""
    return SurgeryWeightLossPage(page)


@pytest.fixture(scope="function")
def weight_loss_program(page):
    """Weight loss program page fixture."""
    return WeightLossProgramPage(page)


@pytest.fixture(scope="function")
def clinically_appropriate(page):
    """Clinically appropriate page fixture."""
    return ClinicallyAppropriatePage(page)


@pytest.fixture(scope="function")
def weight_change_last_year(page):
    """Weight change last year page fixture."""
    return WeightChangeLastYearPage(page)


# ------------------- Test Data Fixtures ------------------- #

@pytest.fixture(scope="function")
def user_data():
    """Generate random test data for the MEDVi qualification flow."""

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
    age_range = rnd.choice(["18-28", "29-39", "40-50", "51-61"])
    reason_for_weight_loss = rnd.choice(["I want to live longer", "I want to feel and look better", "I want to reduce current health issues", "All of these"])
    lose_weight_goal = rnd.choice(["That works for me", "I want it faster", "That's too fast"])
    sleep_routine = rnd.choice(["Pretty Good", "A bit restless", "I don't sleep well"])
    sleep_hours = rnd.choice(["Less than 5 hours", "6-7 hours", "8-9 hours", "More than 9 hours"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    taken_medication = rnd.choice(["Yes, I've taken GLP-1 medication"])
    # , "Yes, I've taken a different medication for weight loss", "No"
    last_dose_days = rnd.choice(["0-5 days", "6-10 days", "11-14 days", "More than 2 weeks ago but within the last 4 weeks", "More than 4 weeks ago"])
    # starting_weight = rnd.randint(75, 110)
    last_three_month_medication = rnd.choice(["Yes", "No"])
    surgery_weight_loss = rnd.choice(["Yes", "No"])
    weight_loss_program = rnd.choice(["Yes", "No"])
    clinically_appropriate = rnd.choice(["Reduce your caloric intake alongside medication", "Increase your physical activity alongside medication", "None of the above"])
    weight_change_last_year = rnd.choice(["Lost a significant amount", "Lost a little", "About the same", "Gained a little"])
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
        "taken_medication": str(taken_medication),
        "last_dose_days": str(last_dose_days),
        "last_three_month_medication": str(last_three_month_medication),
        "surgery_weight_loss": str(surgery_weight_loss),
        "weight_loss_program": str(weight_loss_program),
        "clinically_appropriate": str(clinically_appropriate),
        "weight_change_last_year": str(weight_change_last_year),
     }

    # Log the generated data
    print("🎲 Generated test data:")
    for key, value in data.items():
        print(f"   {key}: {value}")

    return data


# --------