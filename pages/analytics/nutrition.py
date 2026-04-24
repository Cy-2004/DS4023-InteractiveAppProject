import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Nutrition Facts", text_alignment="center")

# sample data
data = {
    "Day": ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],
    "Calories": [2000, 2100, 1900, 2200, 2050, 2300, 2100],
    "Protein": [70, 80, 65, 90, 75, 85, 78],
    "Sugar": [50, 60, 45, 70, 55, 65, 58],
    "Carbohydrates": [250, 270, 240, 290, 260, 300, 275],
    "Fiber": [25, 28, 22, 30, 26, 29, 27]
}

df = pd.DataFrame(data)

st.session_state.nutrition_df = df

# layout
col1, col2 = st.columns([3,1])

# filter
with col2:
    nutrient = st.radio(
        "Choose what nutrient(s) to examine:",
        ["Calories","Protein","Sugar","Carbohydrates","Fiber"]
    )

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
        df["Day"],
        df[nutrient],
        color=colors[nutrient]
    )

    # axis labels
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel(f"{nutrient} ({units[nutrient]})")

    ax.set_xticks(range(len(df["Day"])))
    ax.set_xticklabels(df["Day"])

    st.pyplot(fig)