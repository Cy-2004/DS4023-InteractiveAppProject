import streamlit as st 
import requests 

# get api key from secrets.toml
# api_key = st.secrets["ILIANA_SPOONACULAR_API_KEY"] 
api_key = st.secrets.get("SPOONACULAR_API_KEY")

if not api_key:
    st.error("Missing Spoonacular API key in secrets.toml")
    st.stop()

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
# using ttl=10800 (3 hours) because recipe search results may not change frequently and this allows for a good balance between freshness and performance
@st.cache_data(ttl=10800)
def get_recipes(query='', cuisine=None, intolerances=None, diet=None, prep_time=30, number=20):
    url = f"{base_url}/recipes/complexSearch"

    params = {
        "apiKey": api_key,
        "query": query,
        "instructionsRequired": True,
        "addRecipeNutrition": True,
        "number": number
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


@st.cache_data(ttl=10800)
def get_recipe_info(recipe_ids):
    url = f'{base_url}/recipes/informationBulk'
    params = {
        "apiKey": api_key,
        "ids": ",".join(map(str, recipe_ids)),
        "includeNutrition": True
    }

    try: 
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 
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
        else: 
            st.success(f'API information call was successful')

        # format data now that have checked for errors 
        info_results = {} 
        for recipe in data:
            recipe_id = recipe.get('id') 
            # ingredients 
            ingredients =  [ing.get("original", "")
                for ing in recipe.get("extendedIngredients", [])]

            # nutrition
            wanted_nutrients = ['Calories', 'Protein', 'Sugar', 'Carbohydrates', 'Fiber']
            nutrients = recipe.get("nutrition", {}).get("nutrients", [])
            nutrition = {n["name"]: f"{n['amount']} {n['unit']}"
                for n in nutrients
                if n["name"] in wanted_nutrients}

            info_results[recipe_id] = {
                "ingredients": ingredients,
                "nutrition": nutrition
            }

        return info_results

    # network error 
    except requests.exceptions.RequestException as e :
        st.error(f'API error: {e}')