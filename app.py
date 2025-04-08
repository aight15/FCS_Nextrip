import streamlit as st
import sqlite3
import pandas as pd
import requests
from math import radians, cos, sin, asin, sqrt
import datetime
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def get_temperature_from_meteo(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['current_weather']['temperature']}\u00b0C"
    except:
        pass
    return "N/A"

@st.cache_data
def geocode_city(city):
    """Geocode a city name using Nominatim."""
    geolocator = Nominatim(user_agent="vacation_type_app")
    return geolocator.geocode(city)
# --- VACATION TYPE QUESTIONNAIRE SECTION ---

st.header("Vacation Type")
st.write("Answer the following questions to help us determine your ideal vacation style.")

# Define five categories for vacation type
vacation_categories = {
    "Adventure": [
        "I enjoy outdoor activities and exploring rugged landscapes.",
        "I like trying extreme sports such as hiking, rafting, or rock climbing.",
        "I prefer vacations that are full of adventure and excitement."
    ],
    "Culture": [
        "I enjoy visiting museums and historical landmarks.",
        "Learning about local history and culture is important to me.",
        "I prefer vacations with rich cultural experiences."
    ],
    "Relaxation": [
        "I prefer vacations that allow me to relax and unwind.",
        "Spending quiet time in a calm environment is essential for me.",
        "I value rest and relaxation during my vacation."
    ],
    "Beach": [
        "I love spending time by the sea or on the beach.",
        "Relaxing on a sunny beach is a key element of my ideal vacation.",
        "I enjoy water activities such as swimming or sunbathing."
    ],
    "Nightlife": [
        "I enjoy going out at night and visiting clubs or lively bars.",
        "A vibrant nightlife is an important part of my ideal vacation.",
        "I prefer vacations with plenty of evening entertainment."
    ]
}

# We'll use a scale from 1 to 4:
scale_options = {
    1: "Highly disagree",
    2: "Somewhat disagree",
    3: "Somewhat agree",
    4: "Highly agree"
}

# Initialize dictionary to store category scores
vacation_scores = {category: 0 for category in vacation_categories}

st.write("Please answer each question with a rating from 1 to 4:")
for category, questions in vacation_categories.items():
    st.subheader(category)
    for i, question in enumerate(questions, start=1):
        # Create a unique key for each question using category and index
        response = st.radio(f"{question}", options=[1, 2, 3, 4], index=1, key=f"{category}_q{i}")
        vacation_scores[category] += response

st.write("Your raw vacation type scores:")
st.write(vacation_scores)

# Compute total score and percentages per category
total_points = sum(vacation_scores.values())
vacation_percentages = {}
for cat, score in vacation_scores.items():
    if total_points > 0:
        vacation_percentages[cat] = round((score / total_points) * 100, 1)
    else:
        vacation_percentages[cat] = 0

st.write("Vacation Type Percentages (%):")
st.write(vacation_percentages)

# Plot a radar chart to visualize the scores
def plot_radar_chart(scores):
    categories = list(scores.keys())
    values = list(scores.values())
    # Repeat the first element to close the radar chart
    categories.append(categories[0])
    values.append(values[0])
    
    fig = go.Figure(
        data=[
            go.Scatterpolar(r=values, theta=categories, fill='toself', name="Vacation Profile")
        ]
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 12]  # Maximum score per category (since 3 questions * 4 = 12)
            )
        ),
        showlegend=False
    )
    st.plotly_chart(fig)

plot_radar_chart(vacation_scores)

# Determine recommended distribution if you have a fixed number of activity suggestions per destination (e.g., 10)
total_recommendations = 10
activity_suggestions = {}
for cat, perc in vacation_percentages.items():
    # Compute number of suggestions based on percentage (rounded to nearest integer)
    count = round((perc / 100) * total_recommendations)
    activity_suggestions[cat] = count

st.write("Based on your responses, we recommend:")
st.write(activity_suggestions)
st.write("For example, if you have 60% for Adventure, you'll see 6 adventure-themed suggestions.")

# ==== START: Code before I (ams1231) added changes =====

#Create a Welcoming effect for the user
st.title("Welcome to NexTrip: the app that allows to find the perfect destination")
st.write("The place where you find your next destination")
st.write("The right destination with the right budget and right travel time")
st.write("Choose your criteria and find the perfect destination!")

#enter the name
st.title("Personal data")
title = st.text_input("Name")
subtitle = st.text_input("Surname")

#enter the age
import datetime
min_date=datetime.date(1980,1,1)
max_date=datetime.date.today()
date=st.date_input("select your birthday",min_value=min_date,max_value=max_date)
st.write("My birthday is on the", date)

#enter the adress
street=st.text_input ("Strasse und Hausnummer")
place=st.text_input ("PLZ und Ort")
st.write(street,",",place)

#conclude personal data
st.write("Hi", title, subtitle, "welcome to NexTrip!")
st.write("Let's find the right destination for you")

st.title("Vacation type")
st.write("...")



# slider for budget
st.title("Budget")
st.write("Define your budget!")
budget = st.slider(" Budget you want to spend(CHF)", 0, 10000, 300)
st.write(f"Your budget for this weekend is is: {budget} CHF")

# ==== END: Code before I (ams1231) added changes =====

st.title("Travel Planner")

# Main selection: Plane or Train
travel_mode = st.selectbox("Choose your mode of travel:", ["Plane", "Train"])
st.write(f"I want to travel by {travel_mode}")

city_names = [row[0] for row in cursor.execute("SELECT name FROM cities").fetchall()]
activity_names = [row[0] for row in cursor.execute("SELECT name FROM activities").fetchall()]

if travel_mode == "Plane":
    st.header("✈️ Plane Travel Preferences")

    start_city = st.selectbox("Select your departure city:", city_names)
    #max_price = st.slider("Maximum price you're willing to pay (CHF):", min_value=50, max_value=2000, value=500, step=50)
    max_duration = st.slider("Maximum travel duration (hours):", min_value=1, max_value=6, value=3)
    activity = st.selectbox("Preferred activity:", activity_names)

    st.markdown("### Summary:")
    st.write(f"Traveling from **{start_city}** by **plane**, max duration: **{max_duration}h**, activity: **{activity}**.")

    if 'show_recommendations' not in st.session_state:
        st.session_state.show_recommendations = False
        st.session_state.start_city = None
        #st.session_state.max_price = None
        st.session_state.max_duration = None
        st.session_state.activity = None

    if st.button("Get recommendations"):
        st.session_state.show_recommendations = True
        st.session_state.start_city = start_city
        #st.session_state.max_price = max_price
        st.session_state.max_duration = max_duration
        st.session_state.activity = activity

    if st.session_state.show_recommendations:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (st.session_state.start_city,))
        start_coords = cursor.fetchone()

        if start_coords:
            lat1, lon1 = start_coords
            max_distance = st.session_state.max_duration * 800

            cursor.execute("SELECT id, name, latitude, longitude FROM cities WHERE name != ?", (st.session_state.start_city,))
            cities = cursor.fetchall()

            matching_cities = []
            for city_id, city_name, lat2, lon2 in cities:
                distance = haversine(lat1, lon1, lat2, lon2)
                if distance <= max_distance:
                    cursor.execute('''
                        SELECT description FROM city_activities
                        JOIN activities ON city_activities.activity_id = activities.id
                        WHERE city_activities.city_id = ? AND activities.name = ?
                    ''', (city_id, st.session_state.activity))
                    results = [r[0] for r in cursor.fetchall() if r[0]]
                    if results:
                        matching_cities.append((city_name, lat2, lon2, results))

            st.markdown("### 🔍 Matching Destinations")
            if matching_cities:
                for city_name, lat2, lon2, activities in matching_cities[:10]:
                    temperature = get_temperature_from_meteo(lat2, lon2)
                    st.markdown(f"**{city_name} ({temperature})**")
                    for act in activities:
                        st.write(f"- {act}")
            else:
                st.info("No destinations match your criteria.")

elif travel_mode == "Train":
    st.header("🚆 Train Travel Preferences")

    start_city_train = st.selectbox("Select your departure city:", city_names, key="train_start")
    max_duration_train = st.slider("Maximum travel duration (hours):", min_value=1, max_value=24, value=6, key="train_duration")
    activity_train = st.selectbox("Preferred activity:", activity_names, key="train_activity")

    st.markdown("### Summary:")
    st.write(f"Traveling from **{start_city_train}** by **train**, max duration: **{max_duration_train}h**, activity: **{activity_train}**.")

    if 'show_train_recommendations' not in st.session_state:
        st.session_state.show_train_recommendations = False
        st.session_state.start_city_train = None
        st.session_state.max_duration_train = None
        st.session_state.activity_train = None

    if st.button("Get train recommendations"):
        st.session_state.show_train_recommendations = True
        st.session_state.start_city_train = start_city_train
        st.session_state.max_duration_train = max_duration_train
        st.session_state.activity_train = activity_train

    if st.session_state.show_train_recommendations:
        cursor.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (st.session_state.start_city_train,))
        start_coords = cursor.fetchone()

        if start_coords:
            lat1, lon1 = start_coords
            max_distance = st.session_state.max_duration_train * 100  # 100 km/h for train

            cursor.execute("SELECT id, name, latitude, longitude FROM cities WHERE name != ?", (st.session_state.start_city_train,))
            cities = cursor.fetchall()

            matching_cities = []
            for city_id, city_name, lat2, lon2 in cities:
                distance = haversine(lat1, lon1, lat2, lon2)
                if distance <= max_distance:
                    cursor.execute('''
                        SELECT description FROM city_activities
                        JOIN activities ON city_activities.activity_id = activities.id
                        WHERE city_activities.city_id = ? AND activities.name = ?
                    ''', (city_id, st.session_state.activity_train))
                    results = [r[0] for r in cursor.fetchall() if r[0]]
                    if results:
                        matching_cities.append((city_name, lat2, lon2, results))

            st.markdown("### 🔍 Matching Train Destinations")
            if matching_cities:
                for city_name, lat2, lon2, activities in matching_cities[:10]:
                    temperature = get_temperature_from_meteo(lat2, lon2)
                    st.markdown(f"**{city_name} ({temperature})**")
                    for act in activities:
                        st.write(f"- {act}")
            else:
                st.info("No destinations match your criteria.")
