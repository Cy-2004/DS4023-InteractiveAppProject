import streamlit as st
from api import get_recipes 

st.title("Meals", text_alignment="center")

# session state
if "meals_data" not in st.session_state:
    st.session_state.meals_data = {
        "Breakfast": [
            {'name': 'Oatmeal', 
            'cuisine': 'American',
            'prep_time': '5 mins',
            'ingredients': ['1/2 cup oats', '1 cup water'],
            'directions': ['Boil water', 'Add oats and simmer for 5 mins'],
            'contains': []}
        ], 
        "Lunch": [
            {"name": "Chicken Caesar Salad",
                "cuisine": "Italian",
                "prep_time": "10 mins",
                "ingredients": ["2 cups lettuce", "1 cup shredded chicken", "1 packet croutons", "1.5 tsp parmesan cheese", "2 tbsp caesar dressing"],
                "directions": ["Mix lettuce, shredded chicken, and parmesan cheese.", "Add croutons and drizzle dressing. Mix well."],
                "contains": ["Dairy", "Poultry"]},
            {"name": "Chipotle Chicken & Macaroni Salad",
                "cuisine": "American",
                "prep_time": "35 mins",
                "ingredients": ["Chicken", "Macaroni", "Chipotle sauce"],
                "directions": ["Cook pasta", "Mix with chicken and sauce"],
                "contains": ["Dairy"]}
        ],
        "Dinner": [
            {"name": "Tortilla Soup",
                "cuisine": "Mexican",
                "prep_time": "30 mins",
                "ingredients": ["Broth", "Chicken", "Tortillas"],
                "directions": ["Boil broth", "Add ingredients"],
                "contains": []}
        ],
        # adding other to catch api errors/extra stuff 
        "Other": []
    }

if "deleted_meal" not in st.session_state:
    st.session_state.deleted_meal = None

if "message" not in st.session_state:
    st.session_state.message = None

# message
if st.session_state.message:
    msg_type, msg_text = st.session_state.message

    if msg_type == "success":
        st.success(msg_text)
    elif msg_type == "warning":
        st.warning(msg_text)
    elif msg_type == "info":
        st.info(msg_text)

    st.session_state.message = None

# mealtime selectbox
col1, col2 = st.columns([1,2])
with col1:
    st.markdown("**Choose a mealtime:**")
with col2:
    meal_type = st.selectbox(
        "Meal",
        ["Breakfast","Lunch","Dinner"],
        label_visibility="collapsed",
        key="meal_type_select" # key stores selected meal type
    )

# get user preferences for doing api generate meals 
user_cuisines = st.session_state.get("selected_cuisines", [])
user_allergies = st.session_state.get("allergies_select", [])
user_sensitivities = st.session_state.get("sensitivities_select", [])
user_intolerances = list(set(user_allergies + user_sensitivities)) 
user_other_dietary = st.session_state.get("other_select", None)

# cuisine selectbox
col1, col2 = st.columns([1,2])
with col1:
    st.markdown("**Select a cuisine:**")
with col2:
    # if user has selected cuisines show those, otherwise show all cuisines from meals data
    if user_cuisines:
        cuisines_showing = user_cuisines
    else: 
        cuisines_showing = ["Italian","Asian","Mexican","Indian","American", "French","Mediterranean","Thai","Greek","Spanish"]
    
    cuisine = st.selectbox(
        "",
        ['All'] + cuisines_showing,
        label_visibility="collapsed",
        key="cuisine_select"  # key stores selected cuisine and triggers dependent UI update
    )

all_meals = st.session_state.meals_data.get(meal_type, [])

# filter meals based on selected cuisine
if cuisine == "All":
    meals = all_meals
else:
    meals = [m for m in all_meals if m["cuisine"] == cuisine]

# empty state
if not meals:
    if cuisine == "All":
        st.warning(f"No meals available for {meal_type}.")
    else:
        st.warning(f"No {cuisine} meals available for {meal_type}.")

# if the button is clicked change state
if st.button("Generate Meals", key="generate_meals_btn"):
    st.session_state.generate_meals = True

    with st.spinner("Generating meals..."):
        # api call w user preferences 
        results = get_recipes(
            query='', cuisine=cuisine, intolerances=user_intolerances, 
            diet=user_other_dietary)

        # checking for errors 
        if not results:
            st.error("Failed to retrieve recipes. Please try again.")
            st.stop()

        api_meals = {'Breakfast': [], 'Lunch': [], 'Dinner': [], 'Other': []}
        total_meals = 0
        for r in results.get('results', []):
            # classify meal type 
            types = r.get("dishTypes", [])
            types = [d.lower() for d in types] 
            if any(x in types for x in ["breakfast", "brunch"]):
                meal_type = "Breakfast"
            elif any(x in types for x in ["lunch", "salad", "soup"]):
                meal_type = "Lunch"
            elif any(x in types for x in ["dinner", "main course"]):
                meal_type = "Dinner"
            else:
                meal_type = 'Other'

            # add to api meals list 
            formatted_meal = {
                # saving id for later because need to use it to get nutrient and ingredient info
                'id': r['id'],
                'name': r['title'],
                'cuisine': ", ".join(r.get("cuisines", [])) or "Unknown", 
                'prep_time': f'{r.get('readyInMinutes', 'N/A')} mins',
                'ingredients': [ing['original'] for ing in r.get('extendedIngredients', [])], 
                'directions': r.get('instructions', 'No instructions provided.').split('. '),
                'contains': r.get('diets', []) + r.get('intolerances', [])
            }

            # add meal to api meals data under correct meal type
            api_meals[meal_type].append(formatted_meal)
            total_meals += 1

        # do session state stuff 
        for meal_type, meals_list in api_meals.items():
            st.session_state.meals_data[meal_type].extend(meals_list)
        
        if total_meals > 0:
            st.success(f"{total_meals} meals generated!")
        else:
            st.warning("No meals found with the given preferences.")

    # change state after api call
    st.session_state.generate_meals = False



# display meals depending on meal type 

for i, meal in enumerate(meals):

    label = f"{meal['name']}  •  {meal['cuisine']}  •  Prep Time: {meal['prep_time']}"

    # init toggle state per meal
    edit_key = f"edit_toggle_{meal_type}_{i}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    with st.expander(label):

        # ingredients
        st.markdown("**Ingredients:**")
        for ing in meal["ingredients"]:
            st.write(f"- {ing}")

        # directions
        st.markdown("**Directions:**")
        for step_num, step in enumerate(meal["directions"], 1):
            st.write(f"{step_num}. {step}")

        # action buttons
        col1, col2 = st.columns(2)

        # toggle edit
        with col1:
            if st.button("Edit Ingredients", key=f"edit_btn_{meal_type}_{i}"):
                st.session_state[edit_key] = not st.session_state[edit_key]

        # delete
        with col2:
            if st.button("Delete Meal", key=f"delete_{meal_type}_{i}"):
                st.session_state.deleted_meal = (meal_type, i, meal)
                del st.session_state.meals_data[meal_type][i]
                st.session_state.message = ("warning", "Meal deleted. You can undo below.")
                st.rerun()

        # edit panel
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

# undo delete
if st.session_state.deleted_meal:
    meal_type, index, meal = st.session_state.deleted_meal

    if st.button("Undo Delete"):
        st.session_state.meals_data[meal_type].insert(index, meal)
        st.session_state.deleted_meal = None
        st.session_state.message = ("info", "Meal restored!")
        st.rerun()