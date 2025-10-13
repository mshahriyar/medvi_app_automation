import pytest
import allure
from datetime import datetime


@allure.title("MEDVi Qualification Flow Automation")
@allure.description("This test verifies the complete 'Am I Qualified?' flow across all MEDVi form pages.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.ui
@pytest.mark.regression
def test_am_i_qualified(
    home_page,
    height_weight_page,
    goal_weight,
    gender_and_age,
    experience_illness,
    priority,
    rank,
    metabolic_graph,
    gpl,
    frank_new_man,
    reasons,
    lose_weight,
    analyze_metabolism,
    sleep_check,
    sleep_hours,
    body_review,
    health_conditions,
    additional_health_questions,
    user_data,
):

    allure.dynamic.label("feature", "Qualification Flow")
    allure.dynamic.label("owner", "QA Automation Team")
    allure.dynamic.label("epic", "MEDVi Intake Journey")

    with allure.step("Step 1: Navigate to MEDVi and start qualification flow"):
        home_page.open()
        home_page.click_get_started()

    with allure.step("Step 2: Fill height and weight details"):
        height_weight_page.wait_for_iframe_ready()
        height_weight_page.select_feet(user_data["feet"])
        height_weight_page.select_inches(user_data["inches"])
        height_weight_page.add_weight(user_data["weight"])
        height_weight_page.hit_next_button()

    with allure.step("Step 3: Set goal weight"):
        goal_weight.add_goal_weight(user_data["goal_weight"])
        goal_weight.verify_together_text()
        goal_weight.hit_next_button()

    with allure.step("Step 4: Select gender and age"):
        gender_and_age.select_gender(user_data["gender"])
        gender_and_age.select_age(user_data["age"])
        gender_and_age.hit_next_button()

    with allure.step("Step 5: Select experience illness"):
        experience_illness.select_experience_illness(user_data["experience_illness"])
        experience_illness.hit_next_button()

    with allure.step("Step 6: Set priority goal"):
        priority.select_goal(user_data["priority"])
        priority.hit_next_button()

    with allure.step("Step 7: Verify ranking section"):
        rank.verify_rank()
        rank.hit_next_button()

    with allure.step("Step 8: Verify metabolic graph"):
        metabolic_graph.verify_graph()
        metabolic_graph.hit_next_button()

    with allure.step("Step 9: Verify testimonial section"):
        frank_new_man.verify_recommendation_visible()
        frank_new_man.hit_next_button()

    with allure.step("Step 10: Verify GLP-1 informational content"):
        gpl.wait_for_glp1_graph()
        gpl.verify_glp1_content()
        gpl.hit_next_button()

    with allure.step("Step 11: Select reasons for weight loss"):
        reasons.verify_reasons_heading_visible()
        reasons.select_reason(user_data["reason"])
        reasons.hit_next_button()

    with allure.step("Step 12: Choose weight loss expectations"):
        lose_weight.select_lose_weight(user_data["lose_weight"])
        lose_weight.hit_next_button()

    with allure.step("Step 13: Verify 'Analyze Metabolism' content"):
        analyze_metabolism.verify_analyze_metabolism_content()
        analyze_metabolism.hit_next_button()

    with allure.step("Step 14: Complete sleep routine check"):
        sleep_check.verify_sleep_routine_heading_visible()
        sleep_check.select_sleep_routine(user_data["sleep"])
        sleep_check.hit_next_button()

    with allure.step("Step 15: Set sleep hours"):
        sleep_hours.verify_sleep_heading_and_image()
        sleep_hours.select_sleep_hours(user_data["sleep_hours"])
        sleep_hours.hit_next_button()

    with allure.step("Step 16: Verify body review content"):
        body_review.verify_body_review_content()
        body_review.hit_next_button()

    with allure.step("Step 17: Verify and select health conditions"):
        health_conditions.verify_health_conditions_content()
        health_conditions.verify_and_select_conditions([
            "End-stage liver disease (cirrhosis)",
            "Cancer (active diagnosis, active treatment, or in remission or cancer-free for less than 5 continuous years - does not apply to non-melanoma skin cancer that was considered cured via simple excision)"
        ])
        health_conditions.hit_next_button()

    with allure.step("Step 18: Complete additional health questions"):
        additional_health_questions.verify_page_headings()
        additional_health_questions.verify_all_conditions_visible()
        additional_health_questions.select_conditions([
            "Sleep apnea",
            "Hypertension (high blood pressure)",
            "None of these"
        ])
        additional_health_questions.hit_next_button()

    allure.attach(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name="Test Execution Timestamp",
        attachment_type=allure.attachment_type.TEXT,
    )

    with allure.step("🎉 Final Verification"):
        allure.dynamic.description_html("<b>All MEDVi qualification steps completed successfully.</b>")
