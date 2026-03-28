import pandas as pd
import streamlit as st

@st.cache_data
def load_spending_data():
    # Cached so it doesn't reload every interaction
    return pd.DataFrame({
        "Week": ["Week 1", "Week 2"],
        "Dates": ["3/15-3/21", "3/22-3/28"],
        "Spending ($)": [23.98, 22.45]
    })