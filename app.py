import streamlit as st

#Create a Welcoming effect for the user
st.title("Welcome to NexTrip: the app that allows to find the perfect destination")
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


# slider for budget
st.write("Define your budget!")
budget = st.slider(" Budget you want to spend(CHF)", 0, 1000, 300")
st.write(f"Your budget for this weekend is is: {budget}")
 


