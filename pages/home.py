import streamlit as st
from datetime import date

st.title("Home", text_alignment="center")

# ---------- TODAY'S SCHEDULE ----------
with st.container():
    st.markdown(
        f"<h3 style='text-align:center;'>Today is {date.today().strftime('%A, %B %d, %Y')}</h3>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    meals = {
        "Breakfast": "Yogurt with granola & strawberries",
        "Lunch": "Chipotle Chicken & Macaroni salad",
        "Dinner": "Beef tacos"
    }

    for col, (meal, desc) in zip([col1, col2, col3], meals.items()):
        with col:
            st.markdown(f"**Your {meal.lower()} plan is:**")
            st.write(desc)

            if st.button(f"Edit", key=f"edit_{meal}"):
                st.info(f"Editing {meal}")

            if st.button(f"Delete", key=f"delete_{meal}"):
                st.warning(f"{meal} deleted")

# ---------- LOWER SECTION ----------
left, right = st.columns([1,1])

# ---------- GROCERY LIST ----------
with left:
    with st.container():
        st.markdown(
            "<h3 style='text-align:center;'>This Week’s Grocery List</h3>",
            unsafe_allow_html=True
        )

        items = [
            ("Item 1", 5.30),
            ("Item 2", 10),
            ("Item 3", 7.10),
            ("Item 4", 1.12),
            ("Item 5", 3.99)
        ]

        total = sum(price for _, price in items)

        for name, price in items:
            st.write(f"{name} - ${price}")

        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"**Total: ${round(total,2)}**")
        with col2:
            if st.button("Edit Grocery"):
                st.info("Edit grocery list")

# ---------- TODAY'S STATS ----------
with right:
    with st.container():
        st.markdown(
            "<h3 style='text-align:center;'>Today's Stats</h3>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Calories", "2110")

        with c2:
            st.metric("Protein", "31g")

        with c3:
            st.metric("Spent", "$23")