import streamlit as st

st.title("Dietary Restrictions", text_alignment="center")

# session state
if "dietary" not in st.session_state:
    st.session_state.dietary = {
        "allergies": [],
        "sensitivities": [],
        "other": []
    }

# all options
allergies_options = ["Nuts", "Dairy", "Shellfish", "Eggs", "Soy", "Wheat"]
sensitivities_options = ["Gluten", "Lactose", "Caffeine", "Spicy Foods"]
other_options = [
    "Halal", "Kosher", "Vegetarian", "Vegan",
    "Low Carb", "Sugar Free", "Paleo", "Keto"
]

# allergies
with st.expander("Allergies"):
    st.session_state.dietary["allergies"] = st.multiselect(
        "Choose allergies",
        allergies_options,
        default=st.session_state.dietary["allergies"],
        key="allergies_select"
    )

# sensitivities/intolerances
with st.expander("Sensitivities / Intolerances"):
    st.session_state.dietary["sensitivities"] = st.multiselect(
        "Choose sensitivities",
        sensitivities_options,
        default=st.session_state.dietary["sensitivities"],
        key="sensitivities_select"
    )

# other
with st.expander("Other Restrictions"):
    st.session_state.dietary["other"] = st.multiselect(
        "Choose restrictions",
        other_options,
        default=st.session_state.dietary["other"],
        key="other_select"
    )