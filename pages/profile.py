import streamlit as st

st.title("Profile", text_alignment="center")

DEFAULT_PROFILE = {
    "name": "",
    "age": "",
    "budget": "",
    "prep_time": 30
}

# ---------- SESSION STATE ----------
if "profile" not in st.session_state:
    st.session_state.profile = DEFAULT_PROFILE.copy()

if "msg" not in st.session_state:
    st.session_state.msg = None

# ---------- CALLBACKS ----------
def save_name():
    name = st.session_state["input_name"].strip()
    if name == "" or name.isdigit():
        st.session_state.msg = ("error", "Must enter a name.")
    else:
        st.session_state.profile["name"] = name
        st.session_state.msg = ("success", "Name saved.")

def save_age():
    val = st.session_state["input_age"].strip()
    if not val.isdigit():
        st.session_state.msg = ("error", "Age must be a number.")
    else:
        st.session_state.profile["age"] = int(val)
        st.session_state.msg = ("success", "Age saved.")

def save_budget():
    budget = st.session_state["input_budget"].strip()
    if not budget.isdigit():
        st.session_state.msg = ("error", "Budget must be a number.")
    else:
        st.session_state.profile["budget"] = int(budget)
        st.session_state.msg = ("success", "Budget saved.")


# ---------- MESSAGE DISPLAY ----------
if st.session_state.msg:
    msg_type, msg = st.session_state.msg

    if msg_type == "success":
        st.success(msg)
    else:
        st.error(msg)

    st.session_state.msg = None


# ---------- INPUT ROWS ----------
def input_row(label, key, value, callback):
    col1, col2 = st.columns([1,3], vertical_alignment="center")
    with col1:
        st.markdown(f"**{label}**")
    with col2:
        st.text_input(
            "",
            value=value,
            key=key,
            on_change=callback
        )

input_row("Name:", "input_name", st.session_state.profile["name"], save_name)
input_row("Age:", "input_age", str(st.session_state.profile["age"]), save_age)
input_row("Weekly Budget:", "input_budget", str(st.session_state.profile["budget"]), save_budget)

# ---------- SLIDER ----------
st.markdown("**Maximum Prep Time (min)**")

st.session_state.profile["prep_time"] = st.slider(
    "",
    10, 90,
    value=st.session_state.profile["prep_time"],
    key="prep_slider"
)

# ---------- LOGOUT ----------
st.markdown("---")

col1, col2 = st.columns([1,5])
with col1:
    if st.button("Log Out"):
        # CLEAR EVERYTHING
        st.session_state.clear()

        # RESET DEFAULTS AFTER CLEAR
        st.session_state.profile = DEFAULT_PROFILE.copy()
        st.session_state.input_name = ""
        st.session_state.input_age = ""
        st.session_state.input_budget = ""
        st.session_state.prep_slider = 30

        st.session_state.msg = ("success", "Successfully logged out!")

        st.rerun()