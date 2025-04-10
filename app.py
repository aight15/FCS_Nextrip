import streamlit as st
import googlemaps
import sqlite3
import pandas as pd
import requests
from math import radians, cos, sin, asin, sqrt
import datetime
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import re


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def duration_to_hours(duration_str):
    hours = 0
    minutes = 0

    # Extract numbers using regex
    hours_match = re.search(r"(\d+)\s*hour", duration_str)
    mins_match = re.search(r"(\d+)\s*min", duration_str)

    if hours_match:
        hours = int(hours_match.group(1))
    if mins_match:
        minutes = int(mins_match.group(1))

    total_hours = hours + (minutes / 60)
    return total_hours

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

def get_train_travel_time(origin_city, destination_city):
    api_key = "AIzaSyAAslBkptekhyJR9ZRZMUDKxBFgztgOBCg"
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Request directions using transit mode = train
    directions_result = gmaps.directions(
        origin=origin_city,
        destination=destination_city,
        mode="transit",
        transit_mode="train",
        departure_time="now"  # Can also use a timestamp
    )

    if not directions_result:
        return "No train route found."

    # Extract travel duration
    duration = directions_result[0]['legs'][0]['duration']['text']
    return duration



@st.cache_data
def geocode_city(city):
    """Geocode a city name using Nominatim."""
    geolocator = Nominatim(user_agent="vacation_type_app")
    return geolocator.geocode(city)

# --- Welcoming the user ---
st.title("Welcome to NexTrip: the app that allows to find the perfect destination")
st.write("The place where you find your next destination")
st.write("The right destination with the right budget and right travel time")
st.write("Choose your criteria and find the perfect destination!")

# --- PERSONAL DATA ---
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
street=st.text_input ("Street und Number")
place=st.text_input ("Code und City")
st.write(street,",",place)

#conclude personal data
st.write("Hi", title, subtitle, "welcome to NexTrip!")
st.write("Let's find the right destination for you")


# --- VACATION TYPE QUESTIONNAIRE SECTION ---

st.header("Vacation Type")
st.write("Answer the following questions to help us determine your ideal vacation style.")

# Define five categories for vacation type
vacation_categories = {
    "Nature & Outdoor Adventure": [
        "I prefer vacations that are full of adventure and excitement",
        "Why relax when you can fall off a cliff? I enjoy extreme sports like hiking, rafting, or rock climbing",
        "Luxury is overrated – give me a tent and a fire pit. I don’t mind basic or rustic accommodations",
    ],
    "Cultural & Historical Exploration": [
        "Learning about local history and culture is important to me",
        "Museums are my nightclubs. I get a thrill from visiting museums and cultural sites",   
        ],
    "Relaxation & Wellness": [
        "I value rest and relaxation during my vacation",
        "Work hard, spa harder. I take wellness and self-care very seriously, even while traveling",
        "A vacation without a beach is like a margarita without tequila",
    ],
    "Sports & Active Recreation": [
        "I like staying physically active while on vacation.",
        "I'll relax when I’m dead. I can’t sit still on vacation, I need to move!",
        "Second place is just the first loser. For me, vacations are another arena to challenge myself and come out on top.",
    ],
    "Urban Entertainment & Nightlife": [
        "A vibrant nightlife is an important part of my ideal vacation",
        "I didn’t come all this way to sleep at 9. I love cities with buzzing nightlife",
        "The real culture is in the shopping bags. I experience new cities best through their shops and markets.​",  
    ],
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

# Get the category with the highest percentage
max_category = max(vacation_percentages, key=vacation_percentages.get)
st.session_state["activity"] = max_category

st.write("Based on your responses, we recommend:")
st.write(activity_suggestions)

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

#takes always the first name in each row of data base

city_names = [row[0] for row in cursor.execute("SELECT name FROM cities").fetchall()]
activity_names = [row[0] for row in cursor.execute("SELECT name FROM activities").fetchall()]

#travel mode Plane

if travel_mode == "Plane":
    st.header("✈️ Plane Travel Preferences")
#select departure city, max travel duration and choose activity
    start_city = st.selectbox("Select your departure city:", city_names)
    #max_price = st.slider("Maximum price you're willing to pay (CHF):", min_value=50, max_value=2000, value=500, step=50)
    max_duration = st.slider("Maximum travel duration (hours):", min_value=1, max_value=6, value=3)

    # Find the index of the recommended activity
    default_index = activity_names.index(max_category)

    # Set the selectbox with that index
    activity = st.selectbox("Preferred activity:", activity_names, index=default_index)

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

        #calculation of possible cities in travel time

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
                        # calculate time it takes
                        time_in_hours = round(distance) / 800 # 800 km/h average plane speed
                        # convert to hours and minutes
                        hours = int(time_in_hours)
                        minutes = int(round((time_in_hours - hours) * 60))
                        time_needed = f"{hours} hours {minutes} mins"
                        matching_cities.append((city_name, lat2, lon2, results, time_needed))

            st.markdown("### 🔍 Matching Destinations")
            if matching_cities:
                for city_name, lat2, lon2, activities, time_needed in matching_cities[:15]:
                    temperature = get_temperature_from_meteo(lat2, lon2)
                    st.markdown(f"**{city_name} ({temperature}) Time needed: {time_needed}**")
                    for act in activities:
                        st.write(f"- {act}")
            else:
                st.info("No destinations match your criteria.")

elif travel_mode == "Train":
    st.header("🚆 Train Travel Preferences")

    start_city_train = st.selectbox("Select your departure city:", city_names, key="train_start")
    max_duration_train = st.slider("Maximum travel duration (hours):", min_value=1, max_value=24, value=6, key="train_duration")
    # Find the index of the recommended activity
    default_index = activity_names.index(max_category)
    activity_train = st.selectbox("Preferred activity:", activity_names, index=default_index, key="train_activity")

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
                for city_name, lat2, lon2, activities in matching_cities[:15]:
                    selected_time = st.session_state.max_duration_train
                    travel_time = get_train_travel_time(st.session_state.start_city_train, city_name)
					# if the travel time is below user input
                    if not duration_to_hours(travel_time) > selected_time:
                        temperature = get_temperature_from_meteo(lat2, lon2)
                        st.markdown(f"**{city_name} ({temperature}) Travel time: {get_train_travel_time(st.session_state.start_city_train, city_name)}**")
                        for act in activities:
                        	st.write(f"- {act}")
            else:
                st.info("No destinations match your criteria.")
