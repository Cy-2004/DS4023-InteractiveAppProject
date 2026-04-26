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
sample_data = pd.DataFrame([
    {"Date": last_week_start + timedelta(days=0),
        "Day": "Sun",
        "Meal": "Breakfast",
        "Name": "Oatmeal",
        "nutrition": {'Calories': '150', 'Protein': '5', 'Sugar': '1', 'Carbohydrates': '27', 'Fiber': '9'}}, 
    {"Date": last_week_start + timedelta(days=1),
        "Day": "Mon",
        "Meal": "Breakfast",
        "Name": "Oatmeal",
        "nutrition": {'Calories': '150', 'Protein': '5', 'Sugar': '1', 'Carbohydrates': '27', 'Fiber': '9'}}, 
    {"Date": last_week_start + timedelta(days=2),
        "Day": "Tues",
        "Meal": "Lunch",
        "Name": "Chipotle Chicken & Macaroni Salad",
        "nutrition": {'Calories': '290', 'Protein': '15', 'Sugar': '1', 'Carbohydrates': '30', 'Fiber': '2'}},
    {"Date": last_week_start + timedelta(days=3),
        "Day": "Wed",
        "Meal": "Dinner", 
        "Name": "Chicken Caesar Salad", 
        "nutrition": {'Calories': '400', 'Protein': '22', 'Sugar': '2', 'Carbohydrates': '7', 'Fiber': '1'}},
    {"Date": last_week_start + timedelta(days=4),
        "Day": "Thurs", 
        "Meal": "Lunch", 
        "Name": "Chicken Caesar Salad", 
        "nutrition": {'Calories': '400', 'Protein': '22', 'Sugar': '2', 'Carbohydrates': '7', 'Fiber': '1'}},
    {"Date": last_week_start + timedelta(days=5),
        "Day": "Fri", 
        "Meal": "Breakfast", 
        "Name": "Oatmeal",
        "nutrition": {'Calories': '150', 'Protein': '15', 'Sugar': '1', 'Carbohydrates': '27', 'Fiber': '9'}}, 
    {"Date": last_week_start + timedelta(days=6),
        "Day": "Sat",
        "Meal": "Dinner", 
        "Name": "Chicken Caesar Salad", 
        "nutrition": {'Calories': '400', 'Protein': '22', 'Sugar': '2', 'Carbohydrates': '7', 'Fiber': '1'}},
])

# check session state 
if "nutrition_log" not in st.session_state:
    st.session_state.nutrition_log = sample_data.copy() 
else:
    existing = st.session_state.nutrition_log
    merged = pd.concat([existing, sample_data], ignore_index=True)
    merged = merged.drop_duplicates(subset=['Date', 'Meal', 'Name'],keep='first')

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
    filtered_df[nutrient] = filtered_df["nutrition"].apply(
            lambda x: int(x.get(nutrient, 0)) if isinstance(x, dict) else 0)
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
# remove unnecessary nutrient rows 
cols_dropping = []
if 'Calories' in display_df.columns and nutrient != 'Calories':
    cols_dropping.append('Calories')
if 'Protein' in display_df.columns and nutrient != 'Protein':
    cols_dropping.append('Protein')
if 'Sugar' in display_df.columns and nutrient != 'Sugar':
    cols_dropping.append('Sugar')
if 'Carbohydrates' in display_df.columns and nutrient != 'Carbphydrates':
    cols_dropping.append('Carbohydrates')
if 'Fiber' in display_df.columns and nutrient != 'Fiber':
    cols_dropping.append('Fiber')

display_df.drop(columns=cols_dropping)

st.markdown("Display df")
st.dataframe(display_df)

# expand nested nutrition dict into columns
nutrition_df = display_df["nutrition"].apply(pd.Series)
st.markdown("Nutrition df")
st.dataframe(nutrition_df)

## combine with main dataframe
display_df = pd.concat([display_df.drop(columns=["nutrition", "Meal", "Name", "Week"]), nutrition_df], axis=1)  
if display_df.columns.duplicated().any():
    display_df = display_df.loc[:, ~display_df.columns.duplicated()]

st.dataframe(display_df, use_container_width=True)