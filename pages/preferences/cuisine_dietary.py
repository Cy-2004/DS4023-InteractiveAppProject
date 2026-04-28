import streamlit as st

st.title("Cuisine Preferences", text_alignment="center")

all_cuisines = ["Italian","Asian","Mexican","Indian","American", "French","Mediterranean","Thai","Greek","Spanish"]

# session state
if "dietary" not in st.session_state:
    st.session_state.dietary = {
        "allergies": [],
        "sensitivities": [],
        "other": []
    }

if "selected_cuisines" not in st.session_state:
    # default: all selected
    st.session_state.selected_cuisines = all_cuisines.copy()

if "select_all" not in st.session_state:
    st.session_state.select_all = True

# callbacks
def toggle_select_all():
    if st.session_state.select_all:
        st.session_state.selected_cuisines = all_cuisines.copy()
    else:
        st.session_state.selected_cuisines = []

def update_selected():
    # keep checkbox synced with multiselect
    st.session_state.select_all = (
        set(st.session_state.selected_cuisines) == set(all_cuisines)
    )

# UI
st.checkbox(
    "Select All",
    key="select_all",
    on_change=toggle_select_all
)

selected_cuisines = st.multiselect(
    "Selected Cuisines",
    options=all_cuisines,
    key="selected_cuisines",
    on_change=update_selected
)

st.markdown("---")

st.title("Dietary Restrictions", text_alignment="center")

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