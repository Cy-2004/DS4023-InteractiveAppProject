import streamlit as st
from pages import home, schedule, cuisine, dietary, meals, nutrition, spending, profile

st.set_page_config(page_title="NutriPlanner", layout="wide")

# Sidebar styling
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #1f4e79;
}
.sidebar-text {
    color: white;
    font-size: 16px;
}
.active {
    color: orange;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("NutriPlanner")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Schedule", "Cuisine Preferences", "Dietary Restrictions",
     "Meals", "Nutrition Facts", "Spending", "Profile"]
)

# Routing
if page == "Home":
    home.show()
elif page == "Schedule":
    schedule.show()
elif page == "Cuisine Preferences":
    cuisine.show()
elif page == "Dietary Restrictions":
    dietary.show()
elif page == "Meals":
    meals.show()
elif page == "Nutrition Facts":
    nutrition.show()
elif page == "Spending":
    spending.show()
elif page == "Profile":
    profile.show()