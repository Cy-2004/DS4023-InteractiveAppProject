import streamlit as st

def show():
    st.title("Meals")

    meal_type = st.selectbox("Choose meal", ["Breakfast","Lunch","Dinner"])

    with st.expander("Chicken Caesar Salad"):
        st.write("Ingredients...")
        if st.button("Delete"):
            st.warning("Deleted! Undo?")