import streamlit as st
from api import get_recipes, get_recipe_info
import time 

st.title("Meals", text_alignment="center")

# session state
if "meals_data" not in st.session_state:
    st.session_state.meals_data = {
        "Breakfast": [
            {'id': 1,
            'name': 'Oatmeal', 
            'cuisine': 'American',
            'prep_time': '5 mins',
            'ingredients': ['1/2 cup oats', '1 cup water'],
            'directions': ['Boil water', 'Add oats and simmer for 5 mins'],
            'nutrition': {'Calories': '150', 'Protein': '5g', 'Sugar': '1g', 'Carbohydrates': '27g', 'Fiber': '9g'},
            'contains': []}
        ], 
        "Lunch/Dinner": [
            {"id": 2,
                "name": "Chicken Caesar Salad",
                "cuisine": "Italian",
                "prep_time": "10 mins",
                "ingredients": ["2 cups lettuce", "1 cup shredded chicken", "1 packet croutons", "1.5 tsp parmesan cheese", "2 tbsp caesar dressing"],
                "directions": ["Mix lettuce, shredded chicken, and parmesan cheese.", "Add croutons and drizzle dressing. Mix well."],
                'nutrition': {'Calories': '400', 'Protein': '22g', 'Sugar': '2g', 'Carbohydrates': '7g', 'Fiber': '1g'},
                "contains": ["Dairy", "Poultry"]},
            {"id": 3,
                "name": "Chipotle Chicken & Macaroni Salad",
                "cuisine": "American",
                "prep_time": "35 mins",
                "ingredients": ["Chicken", "Macaroni", "Chipotle sauce"],
                "directions": ["Cook pasta", "Mix with chicken and sauce"],
                "nutrition": {'Calories': '290', 'Protein': '15g', 'Sugar': '1g', 'Carbohydrates': '30g', 'Fiber': '2g'},
                "contains": ["Dairy"]},
            {"id": 4,
                "name": "Tortilla Soup",
                "cuisine": "Mexican",
                "prep_time": "30 mins",
                "ingredients": ["Broth", "Chicken", "Tortillas"],
                "directions": ["Boil broth", "Add ingredients"],
                "nutrition": {'Calories': '270', 'Protein': '20g', 'Sugar': '1g', 'Carbohydrates': '15g', 'Fiber': '2g'},
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
        ["Breakfast","Lunch", "Dinner"],
        label_visibility="collapsed",
        key="meal_type_select" # key stores selected meal type
    )

# classify meal_type for easier recipe filtering later on 
classified_meal_type = ''
if meal_type:
    if meal_type == 'Breakfast':
        classified_meal_type = 'Breakfast'
    else: # else is lunch or dinner 
        classified_meal_type = 'Lunch/Dinner'

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

all_meals = st.session_state.meals_data.get(classified_meal_type, [])

# filter meals based on selected cuisine
if cuisine == "All":
    meals = all_meals
else:
    meals = [m for m in all_meals 
    if cuisine.lower() in m["cuisine"].lower()]

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
        time.sleep(2)
        results = get_recipes(
            query='', cuisine=cuisine, intolerances=user_intolerances, 
            diet=user_other_dietary)

        # checking for errors 
        if not results:
            st.error("Failed to retrieve recipes. Please try again.")  
            st.session_state.generate_meals = False 
            st.stop()

        # missing data
        if not results.get("results"):
            st.warning("No meals matched your preferences.")
            st.session_state.generate_meals = False 
            st.stop()
            
            
        # intializing meals data for api call 
        api_meals = {'Breakfast': [], 'Lunch/Dinner': [],'Other': []}
        total_meals = 0
        existing_ids = {
            "Breakfast": set(),
            "Lunch/Dinner": set(),
            "Other": set()}
        all_existing_ids = set().union(*existing_ids.values())
        
        for classified_type, meals in st.session_state.meals_data.items():
            for meal in meals:
                if "id" in meal:
                    existing_ids[classified_type].add(meal["id"])

        # create new_id list for getting recipe info details 
        new_ids = [
            r.get("id")
            for r in results.get("results", [])
            if r.get("id") not in all_existing_ids
        ]

        new_ids = sorted(set(new_ids))
        if new_ids:
            bulk_details = get_recipe_info(tuple(new_ids))
        else:
            bulk_details = {}

        # for r in results.get('results', []):
        #     recipe_id = r.get("id")
        #     if recipe_id not in existing_ids[classified_type]:
        #         new_ids.append(recipe_id)
        # bulk_details = get_recipe_info(new_ids)

        for r in results.get('results', []):
            # classify meal type 
            types = r.get("dishTypes", [])
            types = [d.lower() for d in types] 
            if any(x in types for x in ["breakfast", "brunch"]):
                classified_type = "Breakfast"
            elif any(x in types for x in ["lunch", "salad", "soup", "dinner", "main course", "main dish"]):
                classified_type = "Lunch/Dinner"
            else: 
                classified_type = "Other"

            # skip if meal already exists in session state meals data
            if r.get("id") in existing_ids[classified_meal_type]:
                st.info(f'{r.get("title")} already exists in your meals')
                continue   

            # pull recipe info from bulk_details list 
            recipe_id = r.get("id")
            deets = bulk_details.get(recipe_id, {})        

            # add to api meals list 
            formatted_meal = {
                # saving id for later because need to use it to get nutrient and ingredient info
                'id': r['id'],
                'name': r['title'],
                'cuisine': ", ".join(r.get("cuisines", [])) or "Unknown", 
                'prep_time': f"{r.get('readyInMinutes', 'N/A')} mins",
                'ingredients': deets.get("ingredients", []),
                'nutrition': deets.get("nutrition", {}),
                'directions': r.get('instructions', 'No instructions provided.').split('. '),
                'contains': r.get('diets', []) + r.get('intolerances', [])
            }

            # add meal to api meals data under correct meal type
            api_meals[classified_type].append(formatted_meal)
            existing_ids[classified_type].add(r.get("id"))
            total_meals += 1
        
        # do session state stuff 
        for classified_type, meals_list in api_meals.items():
            st.session_state.meals_data[classified_type].extend(meals_list)
        
        # print number of meals generated depending on meal type selected 
        if total_meals > 0:
            if meal_type == "Breakfast":
                st.success(f"{len(api_meals['Breakfast'])} breakfast meals generated!")
            elif meal_type == "Lunch":
                st.success(f"{len(api_meals['Lunch/Dinner'])} lunch meals generated!")
            # else: # meal_type == "Dinner"
            #     st.success(f"{len(api_meals['Dinner'])} dinner meals generated!")
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
        # display meal type 
        st.markdown(f"**Meal Type:** {meal_type}")

        # ingredients
        st.markdown("**Ingredients:**")
        for ing in meal["ingredients"]:
            st.write(f"- {ing}")

        # directions
        st.markdown("**Directions:**")
        for step_num, step in enumerate(meal["directions"], 1):
            st.write(f"{step_num}. {step}")

        # nutrition facts 
        st.markdown("**Nutrition Facts:**")
        nutrition = meal.get("nutrition", {})
        if nutrition:
            for nutrient, value in nutrition.items():
                st.write(f"- {nutrient.capitalize()}: {value}")
        else:
            st.write("Nutrition information not available.")

        # contains
        contains = meal.get("contains")
        if contains:
            st.markdown("**Contains:**")
            for ing in meal["contains"]:
                st.write(f"- {ing}")

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