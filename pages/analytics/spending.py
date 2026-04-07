import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.title("Spending", text_alignment="center")

# session state
if "spending_data" not in st.session_state:
    st.session_state.spending_data = pd.DataFrame({
        "Date": pd.date_range(start="2026-01-01", periods=10, freq="7D"),
        "Spending": [20,25,22,30,28,35,40,38,45,50]
    })

if "spending_msg" not in st.session_state:
    st.session_state.spending_msg = None

df = st.session_state.spending_data.copy()
df["Date"] = pd.to_datetime(df["Date"])

# convert to weekly
df["Week"] = df["Date"].dt.to_period("W")
weekly_df = df.groupby("Week")["Spending"].sum().reset_index()

# convert to timestamps for plotting
weekly_df["WeekStart"] = weekly_df["Week"].apply(lambda r: r.start_time)

# layout
col1, col2 = st.columns([3,1])

# slider
with col2:
    min_date = weekly_df["WeekStart"].min().date()
    max_date = weekly_df["WeekStart"].max().date()

    start_date, end_date = st.slider(
        "Choose time interval (weeks):",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        step=timedelta(days=7)
    )

    filtered_weekly = weekly_df[
        (weekly_df["WeekStart"] >= pd.to_datetime(start_date)) &
        (weekly_df["WeekStart"] <= pd.to_datetime(end_date))
    ]

# graph
with col1:
    st.markdown(
        "<h3 style='font-style: italic; text-align: center;'>"
        "Weekly Spending Throughout the Year ($)</h3>",
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots()

    ax.plot(
        filtered_weekly["WeekStart"],
        filtered_weekly["Spending"],
        marker='o',
        color="#1E90FF"
    )

    ax.set_xlabel("Week")
    ax.set_ylabel("Amount ($)")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# add new spending inputs
st.markdown("### Add New Spending")

colA, colB, colC = st.columns([2,2,1])

with colA:
    st.text_input("Amount ($)", key="amount_input")

with colB:
    st.date_input("Date", value=date.today(), key="date_input")

with colC:
    if st.button("Submit"):
        amount = st.session_state.amount_input.strip()

        if amount == "":
            st.session_state.spending_msg = ("error", "Enter an amount.")
        else:
            try:
                val = float(amount)

                new_row = pd.DataFrame({
                    "Date": [pd.to_datetime(st.session_state.date_input)],
                    "Spending": [val]
                })

                st.session_state.spending_data = pd.concat(
                    [st.session_state.spending_data, new_row],
                    ignore_index=True
                )

                st.session_state.spending_msg = ("success", "Spending added!")

            except:
                st.session_state.spending_msg = ("error", "Amount must be a number.")

        st.rerun()

# message
if st.session_state.spending_msg:
    msg_type, msg_text = st.session_state.spending_msg

    if msg_type == "success":
        st.success(msg_text)
    else:
        st.error(msg_text)

    st.session_state.spending_msg = None

# dataframe
st.markdown("### Weekly Spending Table")

display_df = filtered_weekly.copy()
display_df["Week"] = display_df["Week"].astype(str)

display_df = display_df[["Week","Spending"]]
display_df.columns = ["Week", "Spending ($)"]

st.dataframe(display_df, use_container_width=True)