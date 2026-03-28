import streamlit as st
import pandas as pd
from data import load_spending_data

def show():
    st.title("Spending")

    col1, col2 = st.columns([3,1])

    with col2:
        st.slider("Select range", 1, 12)

    with col1:
        df = load_spending_data()
        st.line_chart(df["Spending ($)"])
        st.dataframe(df)

    amount = st.text_input("Enter amount")
    date = st.date_input("Select date")