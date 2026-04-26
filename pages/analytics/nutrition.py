import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta 

st.title("Nutrition Facts", text_alignment="center")

# create sample data 
today = date.today()
this_sunday = today - timedelta(days=(today.weekday() + 1) % 7)
last_week_start = this_sunday - timedelta(days=7)

# "Date": ["2026-04-19", "2026-04-20", "2026-04-21", "2026-04-22", "2026-04-23", "2026-04-24", "2026-04-25"],
sample_data = pd.DataFrame({
    "Date": [last_week_start + timedelta(days=i) for i in range(7)],
    "Day": ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],
    "Meal": ["Breakfast"] * 7,
    "Name": ["Oatmeal"] * 7,
    "Calories": [2000, 2100, 1900, 2200, 2050, 2300, 2100],
    "Protein": [70, 80, 65, 90, 75, 85, 78],
    "Sugar": [50, 60, 45, 70, 55, 65, 58],
    "Carbohydrates": [250, 270, 240, 290, 260, 300, 275],
    "Fiber": [25, 28, 22, 30, 26, 29, 27]})

# check session state 
if "nutrition_log" not in st.session_state:
    st.session_state.nutrition_log = sample_data.copy() 
else:
    existing = st.session_state.nutrition_log
    merged = pd.concat([existing, sample_data], ignore_index=True)
    merged = merged.drop_duplicates(subset=['Date', 'Meal', 'Name', 'Day'],keep='first')

    st.session_state.nutrition_log = merged 


df = st.session_state.nutrition_log.copy() 
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.to_period("W-SUN")

# layout
col1, col2 = st.columns([3,1])

# filter
with col2:
    nutrient = st.radio(
        "Choose what nutrient(s) to examine:",
        ["Calories","Protein","Sugar","Carbohydrates","Fiber"]
    )

    # dropdown for week selection
    week_options = sorted(df["Week"].astype(str).unique())

    selected_week = st.selectbox("Select a week:", sorted(week_options), key='selected_week')


filtered_df = df[df["Week"].astype(str) == selected_week]

# graph
with col1:

    units = {
        "Calories": "kcal",
        "Protein": "g",
        "Sugar": "g",
        "Carbohydrates": "g",
        "Fiber": "g"
    }

    colors = {
        "Calories": "#FF8C00",  
        "Protein": "#2E8B57",    
        "Sugar": "#DC143C",      
        "Carbohydrates": "#1E90FF",      
        "Fiber": "#8A2BE2"       
    }

    # title
    st.markdown(
        f"<h3 style='font-style: italic; text-align: center;'>"
        f"{nutrient} Intake This Week ({units[nutrient]})</h3>",
        unsafe_allow_html=True
    )

    # bar chart
    fig, ax = plt.subplots()

    ax.bar(
        filtered_df["Day"],
        filtered_df[nutrient],
        color=colors[nutrient]
    )

    # axis labels
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel(f"{nutrient} ({units[nutrient]})")

    ax.set_xticks(range(len(filtered_df["Day"])))
    ax.set_xticklabels(filtered_df["Day"])

    st.pyplot(fig)

# add nutrition table below to show this week's all nutrition facts 
st.markdown("### Weekly Nutrition Table")

display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.date

# include all nutrients instead of just one
display_df = display_df[["Date", "Day", "Calories", "Protein", "Sugar", "Carbohydrates", "Fiber"]]

st.dataframe(display_df, use_container_width=True)