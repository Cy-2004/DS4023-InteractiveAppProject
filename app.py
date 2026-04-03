import streamlit as st

# ---------- CONFIG ----------
st.set_page_config(
    page_title="NutriPlanner",
    page_icon="🥗",
    layout="wide"
)

# ---------- CLEAN UI ----------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container {padding-top:1rem;}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "meals" not in st.session_state:
    st.session_state.meals = {
        "Breakfast": "Yogurt",
        "Lunch": "Chicken Salad",
        "Dinner": "Tacos"
    }

# ---------- NAVIGATION ----------
pages = {
    "Main": [
        st.Page("pages/home.py", title="Home", icon="🏠"),
        st.Page("pages/schedule.py", title="Schedule", icon="📅"),
        st.Page("pages/meals.py", title="Meals", icon="🍽️"),
    ],

    "Preferences": [
        st.Page("pages/preferences/cuisine.py", title="Cuisine Preferences", icon="🍜"),
        st.Page("pages/preferences/dietary.py", title="Dietary Restrictions", icon="🥑"),
    ],

    "Analytics": [
        st.Page("pages/analytics/nutrition.py", title="Nutrition Facts", icon="📊"),
        st.Page("pages/analytics/spending.py", title="Spending", icon="💰"),
    ],

    "Account": [
        st.Page("pages/profile.py", title="Profile", icon="👤"),
    ]
}

nav = st.navigation(pages)
nav.run()