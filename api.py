import streamlit as st 
import requests 

# get api key from secrets.toml
api_key = st.secrets["SPOONACULAR_API_KEY"] 

# base url for accessing the api -> get recipes, all info, include nutrition facts
base_url = 'https://api.spoonacular.com'

# import selections from UI pages 
cuisines = st.session_state.get('selected_cuisines')
allergies = st.session_state.get('allergies_select', [])
sensitivities = st.session_state.get('sensitivities_select', [])
# Convert to list if they're not already
if hasattr(allergies, 'tolist'):
    allergies = allergies.tolist()
if hasattr(sensitivities, 'tolist'):
    sensitivities = sensitivities.tolist()
intolerances = allergies.append(sensitivities) 
other_dietary = st.session_state.get('other_select')
print(cuisines)
print(f'allergies: {allergies}')


def get_recipes(query='', cuisine=None, intolerances=None, diet=None, prep_time=30):
    url = f"{base_url}/recipes/complexSearch"

    params = {
        "apiKey": api_key,
        "query": query,
        "instructionsRequired": True,
        "addRecipeNutrition": True
    }

    # possible parameters for the query based on user preferences 
    if cuisine:
        params["cuisine"] = ",".join(cuisine) if isinstance(cuisine, list) else cuisine
    if diet and diet != "None":
        params["diet"] = diet.lower()
    if intolerances:
        params["intolerances"] = ",".join(intolerances)
    if prep_time:
        params['maxReadyTime'] = int(prep_time)

    response = requests.get(url, params=params)
    return response.json()