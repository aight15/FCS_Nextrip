import streamlit as st
import sqlite3
import pandas as pd
import requests
from math import radians, cos, sin, asin, sqrt

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
