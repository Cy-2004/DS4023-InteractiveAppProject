import streamlit as st

def show():
    st.title("Schedule")

    tab1, tab2 = st.tabs(["Meal Schedule", "Class Schedule"])

    with tab1:
        st.write("Weekly Meal Plan")
        st.radio("Select Day", ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"])

    with tab2:
        st.write("Class Schedule")