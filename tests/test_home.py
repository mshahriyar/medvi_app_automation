def test_am_i_qualified(add_height_weight, goal_weight, gender_and_age, experience_illness, priority, rank, user_data):

    add_height_weight.open()
    add_height_weight.click_get_started()
    add_height_weight.wait_for_iframe_ready()

    add_height_weight.select_feet(user_data["feet"])
    add_height_weight.select_inches(user_data["inches"])
    add_height_weight.add_weight(user_data["weight"])
    add_height_weight.hit_next_button()

    goal_weight.add_goal_weight(user_data["goal_weight"])
    goal_weight.hit_next_button()

    # Step 4: Select gender and age
    gender_and_age.select_gender(user_data["gender"])
    gender_and_age.select_age(user_data["age"])
    gender_and_age.hit_next_button()

    # # Step 5: Select experience
    experience_illness.select_experience_illness(user_data["experience_illness"])
    experience_illness.hit_next_button()

    # Step 6: Select priority
    priority.select_goal(user_data["priority"])
    priority.hit_next_button()

    # Step 7: Verify rank
    rank.verify_rank()
    rank.hit_next_button()