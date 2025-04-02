import streamlit as st
st.title("✈️ Welcome to NexTrip: the app that allows to find the perfect destination ✈️")
st.write("The place where you find your next destination")
st.write("The right destination with the right budget and right travel time")
st.write("Choose your criteria and find the perfect destination!")
st.title("Personal data")
st.text_input("Name")
print("hello")




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
    
    response = requests.get(url)
    if response.status_code != 200:
        st.error("❌ Error: Unable to fetch weather data from Open-Meteo.")
        return None
    
    data = response.json()
    if "hourly" in data:
        return data["hourly"]["temperature_2m"][0]  # Get the first hourly temperature
    return None

st.title("✈️ Welcome to NexTrip: the app that allows to find the perfect destination ✈️")
st.write("Choose your criteria and find the perfect destination!")

# Slider for temperature range (minimum and maximum)
temperature_min, temperature_max = st.slider("🌡 Desired Temperature Range (°C)", 
                                             -20, 40, (-5, 30))


# Slider for budget
budget = st.slider("💰 Maximum Budget (€)", 0, 1000, 300)


st.write(f"✅ You are looking for a destination with temperatures between {temperature_min}°C and {temperature_max}°C, and a budget of {budget}€")




# Ask the user for their departure city
departure_city = st.text_input("📍 Where are you traveling from?", "Paris")

# Slider for distance
distance = st.slider("🌍 Maximum Distance you want to travel (km)", 0, 5000, 1500)


# Display the selected maximum distance
st.write(f"✅ You are looking for a destination within {distance} km of your current location.")



city_coords = {
    "Istanbul": (41.0082, 28.9784),
    "Moscow": (55.7558, 37.6173),
    "London": (51.5074, -0.1278),
    "Saint Petersburg": (59.9343, 30.3351),
    "Berlin": (52.5200, 13.4050),
    "Madrid": (40.4168, -3.7038),
    "Rome": (41.9028, 12.4964),
    "Kyiv": (50.4501, 30.5236),
    "Bucharest": (44.4268, 26.1025),
    "Paris": (48.8566, 2.3522),
    "Belgrade": (44.8176, 20.4633),
    "Hamburg": (53.5511, 9.9937),
    "Warsaw": (52.2298, 21.0118),
    "Budapest": (47.4979, 19.0402),
    "Vienna": (48.2082, 16.3738),
    "Munich": (48.1351, 11.5820),
    "Milan": (45.4642, 9.1900),
    "Prague": (50.0755, 14.4378),
    "Sofia": (42.6977, 23.3219),
    "Amsterdam": (52.3676, 4.9041),
    "Stuttgart": (48.7758, 9.1829),
    "Hamburg": (53.5511, 9.9937),
    "Stockholm": (59.3293, 18.0686),
    "Lisbon": (38.7169, -9.1395),
    "Oslo": (59.9139, 10.7522),
    "Athens": (37.9838, 23.7275),
    "Copenhagen": (55.6761, 12.5683),
    "Zürich": (47.3769, 8.5417),
    "Antwerp": (51.2194, 4.4025),
    "Kraków": (50.0647, 19.9450),
    "Minsk": (53.9, 27.5667),
    "Tallinn": (59.4370, 24.7535),
    "Budapest": (47.4979, 19.0402),
    "Helsinki": (60.1699, 24.9384),
    "Chisinau": (47.0105, 28.8638),
    "Belfast": (54.5973, -5.9301),
    "Vilnius": (54.6892, 25.2798),
    "Riga": (56.946, 24.1059),
    "Zagreb": (45.8131, 15.978),
    "Belgrade": (44.8176, 20.4633),
    "Sarajevo": (43.8486, 18.3564),
    "Skopje": (41.9981, 21.4254),
    "Tbilisi": (41.7151, 44.8271),
    "Chisinau": (47.0105, 28.8638),
    "Bucharest": (44.4268, 26.1025),
    "Baku": (40.4093, 49.8671),
    "Dublin": (53.3498, -6.2603),
    "Bristol": (51.4545, -2.5879),
    "Cardiff": (51.4816, -3.1791),
    "Manchester": (53.4808, -2.2426),
    "Leeds": (53.8000, -1.5491),
    "Liverpool": (53.4084, -2.9916),
    "Newcastle upon Tyne": (54.9783, -1.6170),
    "Sheffield": (53.3811, -1.4701),
    "Nottingham": (52.9548, -1.1581),
    "Leicester": (52.6369, -1.1398),
    "Bradford": (53.7956, -1.7599),
    "Coventry": (52.4080, -1.5102),
    "Birmingham": (52.4862, -1.8904),
    "Glasgow": (55.8642, -4.2518),
    "Edinburgh": (55.9533, -3.1883),
    "Moscow": (55.7558, 37.6173),
    "Munich": (48.1351, 11.5820),
    "Rome": (41.9028, 12.4964),
    "Berlin": (52.5200, 13.4050),
    "Vienna": (48.2082, 16.3738),
    "Bucharest": (44.4268, 26.1025),
    "Budapest": (47.4979, 19.0402),
    "Warsaw": (52.2298, 21.0118),
    "Paris": (48.8566, 2.3522),
    "Copenhagen": (55.6761, 12.5683),
    "Stockholm": (59.3293, 18.0686),
    "Sofia": (42.6977, 23.3219),
    "Helsinki": (60.1699, 24.9384),
    "Oslo": (59.9139, 10.7522),
    "Dublin": (53.3498, -6.2603),
    "Prague": (50.0755, 14.4378),
    "Belfast": (54.5973, -5.9301),
    "Ljubljana": (46.0511, 14.5051),
    "Riga": (56.946, 24.1059),
    "Vilnius": (54.6892, 25.2798),
    "Tirana": (41.3275, 19.8189),
    "Chisinau": (47.0105, 28.8638),
    "Zagreb": (45.8131, 15.978),
    "Sarajevo": (43.8486, 18.3564),
    "Skopje": (41.9981, 21.4254),
    "Tbilisi": (41.7151, 44.8271),
    "Zürich": (47.3769, 8.5417),
    "Warsaw": (52.2298, 21.0118),
    "Belgrade": (44.8176, 20.4633),
    "Chisinau": (47.0105, 28.8638),
    "Tbilisi": (41.7151, 44.8271)}



# Fetch coordinates of the departure city using OpenCage API
latitude, longitude = get_coordinates(departure_city)

if latitude and longitude:
    st.write(f"📍 Your current location: {departure_city} ({latitude}, {longitude})")

    matching_destinations = []

    for city_name, (city_lat, city_lon) in city_coords.items():
        # Calculate the distance to the city
        distance_to_city = calculate_distance(latitude, longitude, city_lat, city_lon)

        # If the city is within the selected distance
        if distance_to_city <= distance:
            # Get the temperature for the city
            city_temp = get_temperature_from_meteo(city_lat, city_lon)

            if city_temp:
                # Check if the temperature is within the desired range
                if temperature_min <= city_temp <= temperature_max:
                    matching_destinations.append((city_name, city_temp, distance_to_city))

    # Display matching destinations
    if matching_destinations:
        st.write("🌍 **Recommended Destinations:**")
        for city, temp, dist in matching_destinations:
            st.write(f"- {city} 🌡 {temp}°C, 📏 {int(dist)} km away")
    else:
        st.write("❌ No matching destinations found based on your criteria.")
else:
    st.write("❌ Couldn't find your departure city. Please try again.")


