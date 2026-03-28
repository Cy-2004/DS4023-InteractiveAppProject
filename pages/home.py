import streamlit as st

def show():
    st.title("Home")

    st.subheader("Today's Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Breakfast\nYogurt with granola")
        if st.button("Edit Breakfast"):
            st.write("Edit clicked")
        if st.button("Delete Breakfast"):
            st.warning("Deleted")

    with col2:
        st.info("Lunch\nChicken Salad")
        st.button("Edit Lunch")
        st.button("Delete Lunch")

    with col3:
        st.info("Dinner\nBeef Tacos")
        st.button("Edit Dinner")
        st.button("Delete Dinner")

    st.subheader("Grocery List")
    budget = st.number_input("Weekly Budget", value=50)
    st.write("Total: $27.51")

    st.subheader("Today's Stats")
    c1, c2, c3 = st.columns(3)
    c1.metric("Calories", "2110")
    c2.metric("Protein", "31g")
    c3.metric("Spent", "$23")