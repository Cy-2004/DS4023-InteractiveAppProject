import streamlit as st
import pandas as pd

def show():
    st.title("Nutrition Facts")

    col1, col2 = st.columns([3,1])

    with col2:
        nutrient = st.radio("Select", ["Calories","Protein"])

    with col1:
        st.bar_chart(pd.DataFrame({"Calories":[2000,2100,1900]}))