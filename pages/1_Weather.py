import streamlit as st
from tools.weather_service import WeatherService

st.set_page_config(
    page_title="Weather - Travel Planning Agent",
    page_icon="🌤️",
    layout="wide"
)

st.title("Weather Forecast")

# Initialize weather service
weather_service = WeatherService()

# Weather lookup interface
city = st.text_input("Enter city name for weather forecast")
if city:
    weather_service.display_weather(city)