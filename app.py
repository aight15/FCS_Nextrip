import streamlit as st

#Create a Welcoming effect for the user
st.title("✈️ Welcome to NexTrip: the app that allows to find the perfect destination ✈️")
st.write("The place where you find your next destination")
st.write("The right destination with the right budget and right travel time")
st.write("Choose your criteria and find the perfect destination!")

#enter the name
st.title("Personal data")
title = st.text_input("Vorname")
subtitle = st.text_input("Name")

#enter the age
month=st.selectbox("Monat",("Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"),)
year=st.selectbox("Jahr",("2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","älter als 1998"),)
st.write("Geburtsdatum:", month, year)

#conclude personal data
st.write("Hi", title, subtitle, "welcome to NexTrip!")
st.write("Let's find the right destination for you")

st.title("Vacation type")


# import streamlit as st
import requests
from math import radians, sin, cos, sqrt, atan2  # math formulas


# OpenCage API Key (Replace with your own)
OPENCAGE_API_KEY = "7f1fc5de98b64d8f8de817f01d56eeef"

# Function to fetch coordinates of the departure city
def get_coordinates(city):
    """Fetch latitude and longitude for a given city using OpenCage API."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("❌ Error: Failed to connect to OpenCage API.")
        return None, None

    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        lat = data["results"][0]["geometry"]["lat"]
        lon = data["results"][0]["geometry"]["lng"]
        return lat, lon
    else:
        return None, None

# Function to calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two geographical points."""
    R = 6371  # Radius of the Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Returns the distance in km


# Function to get current temperature for a given city using Open-Meteo API
def get_temperature_from_meteo(lat, lon):
    """Fetch current temperature using Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    
 


