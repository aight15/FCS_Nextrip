import streamlit as st
st.title("✈️ Welcome to NexTrip: the app that allows to find the perfect destination ✈️")
st.write("The place where you find your next destination")
st.write("The right destination with the right budget and right travel time")
st.write("Choose your criteria and find the perfect destination!")
st.subtitle("Personal data")
st.text_input("Name")
print("hello")

#Elias weather
# Function to get current temperature for a given city using Open-Meteo API
def get_temperature_from_meteo(lat, lon):
    """Fetch current temperature using Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    
    response = requests.get(url)
    if response.status_code != 200:
        st.error("❌ Error: Unable to fetch weather data from Open-Meteo.")
        return None
    
    data = response.json()
    if "hourly" in data:
        return data["hourly"]["temperature_2m"][0]  # Get the first hourly temperature
    return None

