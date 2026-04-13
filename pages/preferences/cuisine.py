import streamlit as st

st.title("Cuisine Preferences", text_alignment="center")

all_cuisines = ["Italian","Asian","Mexican","Indian","American", "French","Mediterranean","Thai","Greek","Spanish"]

# session state
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