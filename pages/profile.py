import streamlit as st

def show():
    st.title("Profile")

    name = st.text_input("Name")
    age = st.text_input("Age")
    budget = st.text_input("Weekly Budget")

    prep = st.slider("Max Prep Time", 5, 60)

    if st.button("Log Out"):
        st.rerun()