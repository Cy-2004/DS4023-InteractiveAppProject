import streamlit as st

def show():
    st.title("Dietary Restrictions")

    with st.expander("Allergies"):
        st.multiselect("Select", ["Nuts","Dairy"])

    with st.expander("Other"):
        st.multiselect("Select", ["Vegan","Keto"])