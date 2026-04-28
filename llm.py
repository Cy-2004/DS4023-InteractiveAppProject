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

    # API error handling
    except Exception as e:

        error_msg = str(e).lower()

        # timeout
        if "timeout" in error_msg or "timed out" in error_msg:
            return "The request took too long. Please try again."
        
        # connection error
        if "connection" in error_msg:
            return "Connection issue. Please check your internet and try again."

        # rate limit (429)
        if "429" in error_msg or "rate limit" in error_msg:
            return "Too many requests right now. Please wait a moment and try again."

        # fallback generic error
        return "Something went wrong while contacting the AI. Please try again."
