import streamlit as st
import pandas as pd

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

# constants
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
meals = ["Breakfast","Lunch","Dinner"]

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

    meal_df = pd.DataFrame("", index=meals, columns=days)

    for (day, meal), value in st.session_state.meal_schedule.items():
        meal_df.loc[meal, day] = value

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
            meals_data = st.session_state.get("meals_data", {}) # get user selected meals from meals.py session state 
            meal_list = meals_data.get(selected_meal, [])
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

        if action == "Add/Edit":
            # meal_name = st.text_input("Enter Meal")
            meal_name = meal_choice

            if st.button("Save Meal", key="save_meal_btn"):
                if meal_name is None:
                    st.error("Please enter a meal before saving.")
                else:
                    st.session_state.meal_schedule[(selected_day, selected_meal)] = meal_name
                    st.session_state.message = "Meal saved successfully!"
                    st.toast("Meal added to schedule")
                    st.rerun()

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