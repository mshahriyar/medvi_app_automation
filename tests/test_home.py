import pytest
from datetime import datetime


@pytest.mark.critical
@pytest.mark.ui
@pytest.mark.regression
def test_am_i_qualified(home_page, height_weight_page, goal_weight, gender_and_age, experience_illness, priority, rank, metabolic_graph, gpl, frank_new_man, reasons, lose_weight, analyze_metabolism, sleep_check, sleep_hours, body_review, health_conditions, additional_health_questions, user_data):

    print("🚀 Starting MEDVi Qualification Flow Test")
    print("=" * 50)

    # Step 1: Navigate to MEDVi and click qualification button
    print("Step 1: Navigate to MEDVi and click qualification button")
    home_page.open()
    home_page.click_get_started()
    print("✅ Home page navigation completed successfully")

    # Step 2: Fill height and weight form
    print("Step 2: Fill height and weight form")
    height_weight_page.wait_for_iframe_ready()
    height_weight_page.select_feet(user_data["feet"])
    height_weight_page.select_inches(user_data["inches"])
    height_weight_page.add_weight(user_data["weight"])

    # Verify form was filled correctly
    print("🔍 Verifying form data was entered correctly...")
    print(f"Height: {user_data['feet']}ft {user_data['inches']}in, Weight: {user_data['weight']}lbs")

    height_weight_page.hit_next_button()
    print("✅ Height and weight verification completed successfully")

    # Step 3: Set goal weight
    print("Step 3: Set goal weight")
    goal_weight.add_goal_weight(user_data["goal_weight"])
    goal_weight.verify_together_text()
    goal_weight.hit_next_button()
    print("✅ Goal weight verification completed successfully")
    print(f"Goal Weight: {user_data['goal_weight']}lbs")

    # Step 4: Select gender and age
    print("Step 4: Select gender and age")
    gender_and_age.select_gender(user_data["gender"])
    gender_and_age.select_age(user_data["age"])
    gender_and_age.hit_next_button()
    print("✅ Gender and age verification completed successfully")
    print(f"Gender: {user_data['gender']}, Age: {user_data['age']}")

    # Step 5: Select experience with illness
    print("Step 5: Select experience with illness")
    experience_illness.select_experience_illness(user_data["experience_illness"])
    experience_illness.hit_next_button()
    print("✅ Experience illness verification completed successfully")
    print(f"Experience Illness: {user_data['experience_illness']}")

    # Step 6: Set priority goal
    print("Step 6: Set priority goal")
    priority.select_goal(user_data["priority"])
    priority.hit_next_button()
    print("✅ Priority verification completed successfully")
    print(f"Priority: {user_data['priority']}")

    # Step 7: Select rank
    print("Step 7: Select rank")
    rank.verify_rank()
    print("✅ Rank verification completed successfully")
    rank.hit_next_button()

    # Step 8: Verify metabolic graph
    print("Step 8: Verify metabolic graph")
    metabolic_graph.verify_graph()
    metabolic_graph.hit_next_button()
    print("✅ Graph verification completed successfully")

    # Step 9: Verify testimonial
    print("Step 9: Verify testimonial")
    frank_new_man.hit_next_button()
    print("✅ Recommendation verification completed successfully")

    # Step 10: Verify GLP information
    print("Step 10: Verify GLP information")
    gpl.wait_for_glp1_graph()
    gpl.verify_glp1_content()
    gpl.hit_next_button()
    print("✅ GLP-1 verification completed successfully")

    # Step 11: Select reasons
    print("Step 11: Select reasons")
    reasons.verify_reasons_heading_visible()
    reasons.select_reason(user_data["reason"])
    reasons.hit_next_button()
    print("✅ Reasons selection verification completed successfully")
    print(f"Reasons: {user_data['reason']}")

    # Step 12: Set weight loss expectations
    print("Step 12: Set weight loss expectations")
    lose_weight.select_lose_weight(user_data["lose_weight"])
    lose_weight.hit_next_button()
    print("✅ Lose weight selection verification completed successfully")
    print(f"Weight Loss Expectation: {user_data['lose_weight']}")

    # Step 13: Analyze metabolism
    print("Step 13: Analyze metabolism")
    analyze_metabolism.verify_analyze_metabolism_content()
    analyze_metabolism.hit_next_button()
    print("✅ Analyze metabolism verification completed successfully")

    # Step 14: Sleep check
    print("Step 14: Sleep check")
    sleep_check.verify_sleep_routine_heading_visible()
    sleep_check.select_sleep_routine(user_data["sleep"])
    sleep_check.hit_next_button()
    print("✅ Sleep routine verification completed successfully")

    # Step 15: Set sleep hours
    print("Step 15: Set sleep hours")
    sleep_hours.verify_sleep_heading_and_image()
    sleep_hours.select_sleep_hours(user_data["sleep_hours"])
    sleep_hours.hit_next_button()
    print("✅ Sleep hours verification completed successfully")
    print(f"Sleep Hours: {user_data['sleep_hours']}")

    # Step 16: Body review
    print("Step 16: Body review")
    body_review.verify_body_review_content()
    body_review.hit_next_button()
    print("✅ Body review verification completed successfully")

    # Step 17: Health conditions
    print("Step 17: Health conditions")
    health_conditions.verify_health_conditions_content()
    health_conditions.verify_and_select_conditions([
        "End-stage liver disease (cirrhosis)",
        "Cancer (active diagnosis, active treatment, or in remission or cancer-free for less than 5 continuous years - does not apply to non-melanoma skin cancer that was considered cured via simple excision)"
    ])
    health_conditions.hit_next_button()
    print("✅ Health conditions verification completed successfully")

    # Step 18: Additional health questions
    print("Step 18: Additional health questions")
    additional_health_questions.verify_page_headings()
    additional_health_questions.verify_all_conditions_visible()
    additional_health_questions.select_conditions([
        "Sleep apnea",
        "Hypertension (high blood pressure)",
        "None of these"
    ])
    additional_health_questions.hit_next_button()
    print("✅ Additional health questions verification completed successfully")

    print("\n🎉 All steps completed successfully!")
    print("=" * 50)
