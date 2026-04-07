import streamlit as st
from datetime import date
import pandas as pd

st.title("Home", text_alignment="center")

# session state
if "meals_home" not in st.session_state:
    st.session_state.meals_home = {
        "Breakfast": "Yogurt with granola & strawberries",
        "Lunch": "Chipotle Chicken & Macaroni salad",
        "Dinner": "Beef tacos"
    }

if "grocery_df" not in st.session_state:
    st.session_state.grocery_df = pd.DataFrame({
        "Item": ["Item 1","Item 2","Item 3","Item 4","Item 5"],
        "Price": [5.30,10,7.10,1.12,3.99]
    })

if "home_msg" not in st.session_state:
    st.session_state.home_msg = None

# style
st.markdown("""
<style>
.blue-box {
    background-color:#e6f2ff;
    padding:20px;
    border-radius:12px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# message
if st.session_state.home_msg:
    msg_type, msg = st.session_state.home_msg
    if msg_type == "success":
        st.success(msg)
    elif msg_type == "warning":
        st.warning(msg)
    else:
        st.error(msg)
    st.session_state.home_msg = None

# today's schedule
with st.container():
    st.markdown("<div class='blue-box'>", unsafe_allow_html=True)

    st.markdown(
        f"<h3 style='text-align:center;'>Today is {date.today().strftime('%A, %B %d, %Y')}</h3>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    for col, meal in zip([col1, col2, col3], ["Breakfast","Lunch","Dinner"]):
        with col:

            # init toggle
            toggle_key = f"edit_toggle_{meal}"
            if toggle_key not in st.session_state:
                st.session_state[toggle_key] = False

            current = st.session_state.meals_home.get(meal, "No meal planned yet")

            st.markdown(f"**Your {meal.lower()} plan is:**")
            st.write(current)

            # toggle edit
            if st.button("Edit", key=f"toggle_{meal}"):
                st.session_state[toggle_key] = not st.session_state[toggle_key]

            # edit
            if st.session_state[toggle_key]:
                new_val = st.text_input(
                    "Edit meal",
                    value="" if current == "No meal planned yet" else current,
                    key=f"input_{meal}"
                )

                if st.button("Save", key=f"save_{meal}"):
                    val = st.session_state.get(f"input_{meal}", "").strip()

                    if val == "":
                        st.session_state.home_msg = ("error", f"{meal} cannot be empty.")
                    else:
                        st.session_state.meals_home[meal] = val
                        st.session_state.home_msg = ("success", f"{meal} updated!")
                        st.session_state[f"edit_toggle_{meal}"] = False
                    st.rerun()
                
            # delete
            if st.button("Delete", key=f"delete_{meal}"):
                st.session_state.meals_home[meal] = "No meal planned yet"
                st.session_state.home_msg = ("warning", f"{meal} deleted.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

left, right = st.columns([1,1])

# grocery list
with left:
    with st.container():
        st.markdown("<div class='blue-box'>", unsafe_allow_html=True)

        st.markdown(
            "<h3 style='text-align:center;'>This Week’s Grocery List</h3>",
            unsafe_allow_html=True
        )

        df = st.session_state.grocery_df
        st.dataframe(df, use_container_width=True)

        total = df["Price"].sum()
        st.write(f"**Total: ${round(total,2)}**")

        # toggle edit
        if "edit_grocery" not in st.session_state:
            st.session_state.edit_grocery = False

        if st.button("Edit Grocery"):
            st.session_state.edit_grocery = not st.session_state.edit_grocery
        
        if st.session_state.edit_grocery:
            st.markdown("### Edit Grocery")

            item_name = st.text_input("Item Name", key="item_name")
            price = st.text_input("Price", key="item_price")

            colA, colB, colC = st.columns(3)

            if "grocery_msg" not in st.session_state:
                st.session_state.grocery_msg = None

            # add
            with colA:
                if st.button("Add"):
                    name = item_name.strip()
                    price_val = price.strip()

                    if name == "" or price_val == "":
                        st.session_state.grocery_msg = ("error", "Both fields required.")
                    elif name in df["Item"].values:
                        st.session_state.grocery_msg = ("warning", "Item already exists.")
                    else:
                        try:
                            new_row = pd.DataFrame([[name, float(price_val)]], columns=["Item","Price"])
                            st.session_state.grocery_df = pd.concat([df, new_row], ignore_index=True)
                            st.session_state.grocery_msg = ("success", "Item added!")
                        except:
                            st.session_state.grocery_msg = ("error", "Price must be a number.")
                    st.rerun()

            # edit
            with colB:
                if st.button("Update"):
                    name = item_name.strip()
                    price_val = price.strip()

                    if name == "" or price_val == "":
                        st.session_state.grocery_msg = ("error", "Both fields required.")
                    else:
                        idx = df[df["Item"] == name].index

                        if len(idx) > 0:
                            try:
                                st.session_state.grocery_df.loc[idx[0], "Price"] = float(price_val)
                                st.session_state.grocery_msg = ("success", "Item updated!")
                            except:
                                st.session_state.grocery_msg = ("error", "Price must be a number.")
                        else:
                            st.session_state.grocery_msg = ("warning", "Item not found.")
                    st.rerun()

            # delete
            with colC:
                if st.button("Delete Item"):
                    name = item_name.strip()

                    if name == "":
                        st.session_state.grocery_msg = ("error", "Enter item name.")
                    else:
                        idx = df[df["Item"] == name].index

                        if len(idx) > 0:
                            st.session_state.grocery_df = df.drop(idx[0])
                            st.session_state.grocery_msg = ("warning", "Item deleted.")
                        else:
                            st.session_state.grocery_msg = ("warning", "Item not found.")
                    st.rerun()
            
            # message
            if st.session_state.grocery_msg:
                msg_type, msg = st.session_state.grocery_msg

                if msg_type == "success":
                    st.success(msg)
                elif msg_type == "warning":
                    st.warning(msg)
                else:
                    st.error(msg)

                st.session_state.grocery_msg = None

        st.markdown("</div>", unsafe_allow_html=True)


# today's stats
with right:
    with st.container():
        st.markdown("<div class='blue-box'>", unsafe_allow_html=True)

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
        
        st.markdown("</div>", unsafe_allow_html=True)