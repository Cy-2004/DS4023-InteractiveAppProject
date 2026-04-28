import streamlit as st
import pandas as pd
from datetime import date, timedelta 

st.title("Schedule", text_alignment="center")

# session state
if "meal_schedule" not in st.session_state:
    st.session_state.meal_schedule = {}

if "class_schedule" not in st.session_state:
    st.session_state.class_schedule = {}

if "edit_meal" not in st.session_state:
    st.session_state.edit_meal = False

if "edit_class" not in st.session_state:
    st.session_state.edit_class = False

if "message" not in st.session_state:
    st.session_state.message = None

if "meals_data" not in st.session_state:
    st.session_state.meals_data = {}

if 'nutrition_log' not in st.session_state:
    st.session_state.nutrition_log = pd.DataFrame(columns=["Date", "Day", "Meal", "Name", "nutrition"])

# constants
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
meals = ["Breakfast","Lunch","Dinner"]
# mapping for later session state calling 
MEAL_KEY_MAP = {
    "Breakfast": "Breakfast",
    "Lunch": "Lunch/Dinner",
    "Dinner": "Lunch/Dinner"}

# style
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {
    justify-content: space-around;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stDataFrame"] div {
    white-space: normal !important;
}
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Meal Schedule", "Class Schedule"])

if st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = None

# meal schedule
with tab1:

    col1, col2 = st.columns([6,1])
    with col1:
        st.subheader("Meal Schedule")
    with col2:
        if st.button("Edit Meals"):
            st.session_state.edit_meal = not st.session_state.edit_meal

    # adding date to display 
    from datetime import date, timedelta
    today = date.today()
    start_of_week = today - timedelta(days=(today.weekday() + 1) % 7)
    date_map = {
        day: (start_of_week + timedelta(days=i)).strftime("%m/%d")
        for i, day in enumerate(days)}

    meal_df = pd.DataFrame("",
        index=meals,
        columns=[f"{day}\n{date_map[day]}" for day in days])

    for (day, meal), value in st.session_state.meal_schedule.items():
        meal_df.loc[meal, f"{day}\n{date_map[day]}"] = value

    st.data_editor(meal_df, use_container_width=True, disabled=True)

    # edit panel
    if st.session_state.edit_meal:
        st.markdown("### Edit Meal")

        selected_day = st.radio("Select Day", days, key="meal_day", horizontal=True)

        # dependent dropdown: meal options depend on meal type
        col1, col2 = st.columns([1,2])
        with col1:
            selected_meal = st.selectbox("Select Meal", meals, key="meal_type")
        with col2:
            meal_key = MEAL_KEY_MAP.get(selected_meal, selected_meal) # get user selected meals from meals.py session state
            meal_list = st.session_state.meals_data.get(meal_key, [])
            meal_names = [meal["name"] for meal in meal_list] 

            if not meal_names:
                st.warning("No meal options available yet. Go to the Meals page and generate some first.")
                meal_choice = None

            else:
                meal_choice = st.selectbox(
                    "Choose Meal",
                    meal_names, # depends on list of users generated meals 
                    key="meal_option_select" # key ensures correct update when meal type changes
                )

        action = st.radio("Action", ["Add/Edit","Delete"], key="meal_action", horizontal=True)

        # function for save meal to perform callback on 
        def save_meal():
            if meal_choice is None:
                st.error("Please enter a meal before saving.")
                return 
            # save to schedule 
            st.session_state.meal_schedule[(selected_day, selected_meal)] = meal_choice 
            
            # save all meal info
            selected_meal_data = next(
                (m for m in meal_list if m["name"].strip().lower() == meal_choice.strip().lower()), None)

            if selected_meal_data:
                # convert day to actual date
                start_of_week = date.today() - timedelta(days=(date.today().weekday() + 1) % 7)
                day_index = days.index(selected_day)
                meal_date = start_of_week + timedelta(days=day_index)

                # st.write("selected meal data", selected_meal_data)
                # create new row
                new_row = pd.DataFrame([
                    {"Date": pd.to_datetime(meal_date),
                    "Day": selected_day,
                    "Meal": selected_meal,
                    "Name": meal_choice,
                    "nutrition": selected_meal_data.get("nutrition", None)}
                   ])

                # append to nutrition log
                st.session_state.nutrition_log = pd.concat(
                    [st.session_state.nutrition_log, new_row],
                    ignore_index=True)
                st.session_state.message = "Meal saved successfully!"
                st.toast("Meal added to schedule")

            else:
                st.error("Meal nutrition not found.")
                return 

        if action == "Add/Edit":
            meal_name = meal_choice

            st.button("Save Meal", key="save_meal_btn", on_click=save_meal)

        else:
            if st.button("Delete Meal", key="delete_meal_btn"):
                st.session_state.meal_schedule.pop((selected_day, selected_meal), None)
                st.session_state.message = "Meal deleted successfully!"
                st.rerun()

# class schedule
with tab2:

    col1, col2 = st.columns([6,1])
    with col1:
        st.subheader("Class Schedule")
    with col2:
        if st.button("Edit Classes"):
            st.session_state.edit_class = not st.session_state.edit_class

    # dynamic time range
    default_hours = list(range(8,17))

    used_hours = [h for (_, h) in st.session_state.class_schedule.keys()]

    if used_hours:
        min_hour = min(min(used_hours), 8)
        max_hour = max(max(used_hours)+1, 17)
    else:
        min_hour, max_hour = 8, 17

    hours = list(range(min_hour, max_hour))

    time_labels = [f"{h}:00-{h+1}:00" for h in hours]
    class_df = pd.DataFrame("", index=time_labels, columns=days)

    for (day, hour), value in st.session_state.class_schedule.items():
        label = f"{hour}:00-{hour+1}:00"
        if label in class_df.index:
            class_df.loc[label, day] = value

    st.data_editor(class_df, use_container_width=True, disabled=True)

    # edit panel
    if st.session_state.edit_class:
        st.markdown("### Edit Schedule")

        selected_day = st.radio("Select Day", days, key="class_day", horizontal=True)

        selected_hour = st.slider(
            "Select Time (hour)",
            0, 23, 8,
            step=1
        )

        action = st.radio("Action", ["Add/Edit","Delete"], key="class_action", horizontal=True)

        if action == "Add/Edit":
            event = st.text_input("Enter Activity")

            if st.button("Save Event", key="save_event_btn"):
                if event.strip() == "":
                    st.error("Please enter an activity before saving.")
                else:
                    st.session_state.class_schedule[(selected_day, selected_hour)] = event
                    st.session_state.message = "Event saved successfully!"
                    st.rerun()

        else:
            if st.button("Delete Event", key="delete_event_btn"):
                st.session_state.class_schedule.pop((selected_day, selected_hour), None)
                st.session_state.message = "Event deleted successfully!"
                st.rerun()