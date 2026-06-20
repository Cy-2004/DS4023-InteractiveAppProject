# NutriPlanner

NutriPlanner is an interactive meal planning and nutrition tracking web application built with **Streamlit**. It helps users organize weekly meals, manage dietary preferences, monitor nutrition and grocery spending, and generate personalized recipe recommendations using the Spoonacular API. The application also includes a Gemini-powered assistant that answers questions about nutrition data within the app.

## Features

### Home Dashboard

* View today's breakfast, lunch, and dinner plans
* Edit or delete scheduled meals
* Manage a weekly grocery list with item and price updates
* Track grocery totals against a weekly budget
* View daily nutrition and spending summaries

### Schedule Management

* Create and edit weekly meal schedules
* Maintain a class/activity schedule
* Assign meals to specific days and mealtimes
* Dynamic editing interface with expandable controls

### Meal Explorer

* Browse meals by mealtime and cuisine
* Generate personalized recipes using the Spoonacular API
* View ingredients, directions, preparation time, and nutrition facts
* Edit ingredient lists and remove or restore meals

### Preferences

* Select preferred cuisines
* Configure allergies, sensitivities, intolerances, and dietary restrictions
* Apply preferences when generating recipes

### Nutrition Analytics

* Visualize weekly nutrition intake with interactive bar charts
* Track calories, protein, sugar, carbohydrates, and fiber
* Compare intake across days of the week

### Spending Tracker

* Record grocery spending over time
* View weekly spending trends in an interactive line chart
* Filter spending history by date range
* Review summarized spending in tabular format

### NutriPlanner Assistant

* Powered by the Gemini API
* Answers questions about nutrition information using application data
* Uses prompt engineering techniques including role/persona prompting and chain-of-thought guidance
* Maintains persistent chat history across reruns

## Technologies Used

* Python
* Streamlit
* pandas
* matplotlib
* Spoonacular API
* Google Gemini API
* Requests

## Project Structure

```text
NutriPlanner/
│
├── app.py
├── api.py
├── llm.py
├── data.py
├── pages/
│   ├── home.py
│   ├── meals.py
│   ├── schedule.py
│   ├── profile.py
│   ├── analytics/
│   │   ├── nutrition.py
│   │   └── spending.py
│   └── preferences/
│       ├── cuisine.py
│       └── dietary.py
└── .streamlit/
    └── secrets.toml
```

## Link to deployed app

https://bz58qe2ves8crmekdpnuqb.streamlit.app/

If you would like to run it locally, follow the steps below:

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd NutriPlanner
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file and add your API keys:

```toml
SPOONACULAR_API_KEY = "your_spoonacular_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```

4. Run the application:

```bash
streamlit run app.py
```

## Usage

* Set your profile information, including weekly budget and preferred preparation time.
* Configure cuisine preferences and dietary restrictions.
* Generate recipes based on your preferences.
* Add meals to your schedule and manage your grocery list.
* Explore nutrition and spending analytics through interactive visualizations.
* Ask the integrated NutriPlanner Assistant questions such as:

  * "What are the total calories I consumed this week?"
  * "Summarize my nutrition data."
  * "How does my calorie intake compare across the week?"

## Key Highlights

* Multi-page interactive Streamlit application
* Session state for persistent user interactions
* External API integration for recipe generation and LLM-powered assistance
* Interactive charts and editable data tables
* Adaptive UI with callbacks, expandable sections, and dependent controls
* Secure API key management using Streamlit secrets
