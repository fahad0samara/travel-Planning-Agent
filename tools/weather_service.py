import requests
import streamlit as st
from datetime import datetime
from difflib import get_close_matches

class WeatherService:
    def __init__(self):
        self.api_key = "7ebfa50639433b69233dddbc7d6295fe"
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_weather_forecast(self, city: str):
        """Get 5-day weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Process and format the forecast data
            forecasts = []
            for item in data['list'][:5]:  # Get next 5 days
                forecast = {
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'temp': round(item['main']['temp']),
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                }
                forecasts.append(forecast)

            return forecasts
        except Exception as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
                # Try to suggest similar city names
                common_cities = ["Cyprus", "Paris", "London", "New York", "Tokyo", "Dubai", "Singapore", "Rome", "Berlin"]
                suggestions = get_close_matches(city, common_cities, n=3, cutoff=0.6)
                
                error_msg = f"City '{city}' not found."
                if suggestions:
                    error_msg += f"\nDid you mean one of these?\n- {', '.join(suggestions)}"
                st.error(error_msg)
            else:
                st.error(f"Error fetching weather data: {str(e)}")
            return None

    def display_weather(self, city: str):
        """Display weather forecast in Streamlit"""
        forecasts = self.get_weather_forecast(city)
        if forecasts:
            st.subheader(f"5-Day Weather Forecast for {city}")
            cols = st.columns(5)
            for i, forecast in enumerate(forecasts):
                with cols[i]:
                    st.write(forecast['date'])
                    st.image(f"http://openweathermap.org/img/w/{forecast['icon']}.png")
                    st.write(f"{forecast['temp']}°C")
                    st.write(forecast['description'])