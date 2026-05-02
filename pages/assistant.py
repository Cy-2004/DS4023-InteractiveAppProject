import streamlit as st
import pandas as pd
from llm import ask_gemini

st.title("NutriPlanner Assistant 🤖")

# clear chat functionality
def clear_chat():
    st.session_state.messages = [] # reset chat history
    if "chat" in st.session_state:
        del st.session_state["chat"] # clear any cached LLM state if used later

st.button("Clear Chat", on_click=clear_chat)  # no st.rerun used

# pull data from clean nutrition log from nutrition page
df = st.session_state.get("clean_nutri_log")

if df is None:
    st.warning("No nutrition data available yet. Visit Nutrition page first.")
    st.stop()
nutri_summary = dict(zip(df["Day"], df["Calories"]))


# pull meals data w just name, type, and nutri facts 
mr = st.session_state.get("meals_data", {})
mr2 = []
for meal_type, meals in mr.items():
    for m in meals:
        mr2.append({
            "name": m["name"],
            "cuisine": m.get("cuisine", "Unknown"),
            "meal_type": meal_type,
            "nutrition": m.get("nutrition", {})
        })

# limit size (VERY IMPORTANT)
meals_rec = str(mr2[:30])

# system prompt
system_prompt = f"""
You are NutriPlanner Assistant, a nutrition and meal recommendation assistant built into a personal meal planning app.

Your role:
- Help users understand their nutrition, meals, and spending data
- Answer ONLY using the app's data provided below
- Do NOT make up data
- Be concise and clear

Nutrition data summary (last week):
{nutri_summary}

Meal recommendation data:
{meals_rec}

When answering:
- Show the final answer clearly
- Briefly explain how you got it (no long reasoning)
"""

# chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
if user_input := st.chat_input("Ask about your nutrition..."):

    # input validation
    if not user_input.strip(): # empty or whitespace
        st.warning("Please enter a valid question.")
        st.stop()

    if len(user_input) > 2000: # long prompt warning
        st.warning("Your question is very long. Consider shortening it.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # classify prompt as nutrition or meal recommendation
    intent_prompt = f"""
    Classify the user input as one of these: 
        - nutrition_question 
        - meal_recommendation
    User input: {user_input}
    Return only the label
    """

    with st.spinner("Understanding request..."):
        intent = ask_gemini(system_prompt, intent_prompt).strip()

    # chain of thought prompt
    if "nutrition" in intent:
        prompt = f"""
        Answer the question using the nutri_summary data.

        Think step-by-step:
        1. Identify daily values
        2. Sum all values together
        3. Give final answer

        Question: {user_input}
        """

    else: # meal rec 
    # structured output prompt 
        prompt = f"""
        You are a meal ranking system.

        ONLY use the meals provided in the meals_rec data.

        Return exactly this format:

        1. Meal Name — reason (nutrition-based)
        2. Meal Name — reason
        3. Meal Name — reason

        Prioritize:
        - Protein if mentioned
        - Calories if mentioned
        - Meal type if mentioned

        Meals:
        {meals_rec}

        User request:
        {user_input}
        """
 
    # loading spinner
    with st.spinner("Thinking..."): # shows app is working
        reply = ask_gemini(system_prompt, prompt)

    # keyword-based prompt injection defense
    suspicious_phrases = ["ignore previous instructions", "disregard", "new role"]
    if any(phrase in user_input.lower() for phrase in suspicious_phrases):
        reply = "I can only help with nutrition and meal recommemdation questions."

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)
