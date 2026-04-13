import streamlit as st 
import requests 

# get api key from secrets.toml
api_key = st.secrets["ILIANA_SPOONACULAR_API_KEY"] 

# base url for accessing the api -> get recipes, all info, include nutrition facts
base_url = 'https://api.spoonacular.com'

# import selections from UI pages 
cuisines = st.session_state.get('selected_cuisines')
allergies = st.session_state.get('allergies_select', [])
sensitivities = st.session_state.get('sensitivities_select', [])
intolerances = list(set(allergies + sensitivities)) 
other_dietary = st.session_state.get('other_select')
print(cuisines)
print(f'allergies: {allergies}')


# caching API responses to reduce redundant calls and respect API rate limits
# using ttl=3600 (1 hour) because recipe search results may not change frequently and this allows for a good balance between freshness and performance
@st.cache_data(ttl=3600)
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
    
    try: 
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        # for invalid API key 
        if response.status_code == 401: 
            st.warning('API key is missing or invalid. ')
        # not found error 
        elif response.status_code == 404:
            st.warning('No results found for your search')
        # rate limit 
        elif response.status_code == 429:
            st.warning('API rate limit exceeded. Please try again later.')
        
        # empty results 
        elif not data.get('results'):
            st.warning('Your search returned no results.')
            data = [] 

        else: 
            st.success(f'API recipe call was successful')
        return data 

    # network error 
    except requests.exceptions.RequestException:
        st.error("Network error. Please check your internet connection.")