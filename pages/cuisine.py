import streamlit as st

def show():
    st.title("Cuisine Preferences")

    col1, col2 = st.columns(2)

    selected = col1.multiselect("Selected", ["Italian","Asian"])
    more = col2.multiselect("More", ["Mexican","Indian"])