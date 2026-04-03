import streamlit as st

st.title("Meals", text_alignment="center")

# ---------- SESSION STATE ----------
if "meals_data" not in st.session_state:
    st.session_state.meals_data = {
        "Lunch": [
            {
                "name": "Chicken Caesar Salad",
                "cuisine": "Italian",
                "time": "10 mins",
                "ingredients": ["2 cups lettuce", "1 cup shredded chicken", "1 packet croutons", "1.5 tsp parmesan cheese", "2 tbsp caesar dressing"],
                "directions": ["Mix lettuce, shredded chicken, and parmesan cheese.", "Add croutons and drizzle dressing. Mix well."],
                "contains": ["Dairy", "Poultry"]
            },
            {
                "name": "Chipotle Chicken & Macaroni Salad",
                "cuisine": "American",
                "time": "35 mins",
                "ingredients": ["Chicken", "Macaroni", "Chipotle sauce"],
                "directions": ["Cook pasta", "Mix with chicken and sauce"],
                "contains": ["Dairy"]
            },
            {
                "name": "Tortilla Soup",
                "cuisine": "Hispanic",
                "time": "30 mins",
                "ingredients": ["Broth", "Chicken", "Tortillas"],
                "directions": ["Boil broth", "Add ingredients"],
                "contains": []
            }
        ]
    }

if "deleted_meal" not in st.session_state:
    st.session_state.deleted_meal = None

if "message" not in st.session_state:
    st.session_state.message = None

# ---------- GLOBAL MESSAGE ----------
if st.session_state.message:
    msg_type, msg_text = st.session_state.message

    if msg_type == "success":
        st.success(msg_text)
    elif msg_type == "warning":
        st.warning(msg_text)
    elif msg_type == "info":
        st.info(msg_text)

    st.session_state.message = None

# ---------- SELECTBOX ----------
col1, col2 = st.columns([1,2])
with col1:
    st.markdown("**Choose a mealtime:**")
with col2:
    meal_type = st.selectbox(
        "",
        ["Breakfast","Lunch","Dinner"],
        label_visibility="collapsed"
    )

meals = st.session_state.meals_data.get(meal_type, [])

# ---------- EMPTY STATE ----------
if not meals:
    st.warning("No meals currently.")
    if st.button("Generate Meals"):
        st.info("Meals generated (placeholder)")
    st.stop()

# ---------- DISPLAY MEALS ----------
for i, meal in enumerate(meals):

    label = f"{meal['name']}  •  {meal['cuisine']}  •  Total Time: {meal['time']}"

    # init toggle state per meal
    edit_key = f"edit_toggle_{meal_type}_{i}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    with st.expander(label):

        # INGREDIENTS
        st.markdown("**Ingredients:**")
        for ing in meal["ingredients"]:
            st.write(f"- {ing}")

        # DIRECTIONS
        st.markdown("**Directions:**")
        for step_num, step in enumerate(meal["directions"], 1):
            st.write(f"{step_num}. {step}")

        # CONTAINS (optional)
        if meal["contains"]:
            st.markdown("**Contains:**")
            for item in meal["contains"]:
                st.write(f"- {item}")

        # ---------- ACTION BUTTONS ----------
        col1, col2 = st.columns(2)

        # TOGGLE EDIT
        with col1:
            if st.button("Edit Ingredients", key=f"edit_btn_{meal_type}_{i}"):
                st.session_state[edit_key] = not st.session_state[edit_key]

        # DELETE
        with col2:
            if st.button("Delete Meal", key=f"delete_{meal_type}_{i}"):
                st.session_state.deleted_meal = (meal_type, i, meal)
                del st.session_state.meals_data[meal_type][i]
                st.session_state.message = ("warning", "Meal deleted. You can undo below.")
                st.rerun()

        # ---------- EDIT PANEL (TOGGLED) ----------
        if st.session_state[edit_key]:
            st.markdown("### Edit Ingredients")

            new_ingredients = st.text_area(
                "Edit ingredients (one per line)",
                "\n".join(meal["ingredients"]),
                key=f"text_{meal_type}_{i}"
            )

            if st.button("Save Changes", key=f"save_{meal_type}_{i}"):
                updated = [x.strip() for x in new_ingredients.split("\n") if x.strip()]

                if not updated:
                    st.error("Ingredients cannot be empty.")
                else:
                    st.session_state.meals_data[meal_type][i]["ingredients"] = updated
                    st.session_state.message = ("success", "Ingredients updated!")
                    st.rerun()

        # # EDIT
        # with col1:
        #     if st.button("Edit Ingredients", key=f"edit_{meal_type}_{i}"):
        #         new_ingredients = st.text_area(
        #             "Edit ingredients (one per line)",
        #             "\n".join(meal["ingredients"]),
        #             key=f"text_{meal_type}_{i}"
        #         )
        #         if st.button("Save Changes", key=f"save_{meal_type}_{i}"):
        #             updated = [x.strip() for x in new_ingredients.split("\n") if x.strip()]

        #             if not updated:
        #                 st.error("Ingredients cannot be empty.")
        #             else:
        #                 st.session_state.meals_data[meal_type][i]["ingredients"] = updated
        #                 st.session_state.message = ("success", "Ingredients updated!")
        #                 st.rerun()

        # # DELETE
        # with col2:
        #     if st.button("Delete Meal", key=f"delete_{meal_type}_{i}"):

        #         st.session_state.deleted_meal = (meal_type, i, meal)
        #         del st.session_state.meals_data[meal_type][i]

        #         st.session_state.message = ("warning", "Meal deleted. You can undo below.")
        #         st.rerun()


# ---------- UNDO DELETE ----------
if st.session_state.deleted_meal:
    meal_type, index, meal = st.session_state.deleted_meal

    if st.button("Undo Delete"):
        st.session_state.meals_data[meal_type].insert(index, meal)
        st.session_state.deleted_meal = None
        st.session_state.message = ("info", "Meal restored!")
        st.rerun()