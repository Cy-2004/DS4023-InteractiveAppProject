import streamlit as st
import google.generativeai as genai

# load API key
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API key in secrets.toml")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def ask_gemini(system_prompt, user_prompt):
    try:
        response = model.generate_content([system_prompt,user_prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"