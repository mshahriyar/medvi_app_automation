
import logging
import os
import random as rnd
import pytest
from config.config import BASE_URL
from pages.experience_illness import ExperienceIllnessPage
from pages.gender_and_age import GenderAndAgePage
from pages.height_and_weight import AddHeightAndWeight
from pages.goal_weight import GoalWeightPage
from pages.priority import PriorityPage
import csv
from datetime import datetime

from pages.rank import RankPage



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
    weight = str(rnd.randint(100, 300))   # 100–300 lbs
    goal_weight = str(rnd.randint(90, int(weight) - 20))

    # Demographics
    gender = rnd.choice(["Male", "Female"])
    experience_illness = rnd.choice(["Low Libido or Erectile Dysfunction ", "Hair Loss", "Skin Issues", "Cognition Issues", "None of these"])
    priority = rnd.choice(["Lose Weight", "Gain Muscle", "Maintain My Current Body"])
    age_range = rnd.choice(["18–28", "29–39", "40-50", "51–61", "62+"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "timestamp": timestamp,
        "feet": feet,
        "inches": inches,
        "weight": weight,
        "goal_weight": goal_weight,
        "gender": gender,
        "age": age_range,
        "experience_illness": experience_illness,
        "priority": priority,
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


