import requests
import logging
import os
from datetime import datetime

# OpenWeatherMap API configuration
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_HARDCODED_OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"

def get_weather_data(location):
    """Get current weather data for a location"""
    try:
        # Get current weather
        current_url = f"{BASE_URL}/weather"
        params = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(current_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Get forecast data
            forecast_data = get_forecast_data(location)
            
            weather_info = {
                'location': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'uv_index': None,  # Would need separate API call
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'forecast': forecast_data
            }
            
            # Add agricultural recommendations
            weather_info['farming_advice'] = get_farming_advice(weather_info)
            
            return weather_info
        else:
            logging.error(f"Weather API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in weather service: {e}")
        return None

def get_forecast_data(location):
    """Get 5-day weather forecast"""
    try:
        forecast_url = f"{BASE_URL}/forecast"
        params = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(forecast_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            forecast = []
            
            # Get daily forecasts (every 24 hours)
            for i in range(0, min(len(data['list']), 40), 8):  # Every 8th item (24 hours)
                item = data['list'][i]
                forecast.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'day': datetime.fromtimestamp(item['dt']).strftime('%A'),
                    'temperature': round(item['main']['temp']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                })
            
            return forecast[:5]  # Return max 5 days
        else:
            return []
            
    except Exception as e:
        logging.error(f"Error fetching forecast data: {e}")
        return []

def get_farming_advice(weather_data):
    """Generate farming advice based on weather conditions"""
    advice = []
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    wind_speed = weather_data['wind_speed']
    description = weather_data['description'].lower()
    
    # Temperature-based advice
    if temp < 5:
        advice.append("⚠️ Frost risk: Protect sensitive plants and consider covering crops.")
    elif temp > 35:
        advice.append("🌡️ High temperature: Increase watering frequency and provide shade for sensitive plants.")
    elif 15 <= temp <= 25:
        advice.append("🌱 Ideal growing conditions: Good time for planting and outdoor activities.")
    
    # Humidity-based advice
    if humidity > 80:
        advice.append("💧 High humidity: Monitor for fungal diseases and ensure good air circulation.")
    elif humidity < 30:
        advice.append("🏜️ Low humidity: Increase irrigation and consider mulching to retain moisture.")
    
    # Wind-based advice
    if wind_speed > 10:
        advice.append("💨 Strong winds: Secure tall plants and protect greenhouse structures.")
    
    # Weather condition advice
    if 'rain' in description:
        advice.append("🌧️ Rainy conditions: Good for soil moisture but watch for waterlogging.")
    elif 'clear' in description or 'sunny' in description:
        advice.append("☀️ Clear skies: Excellent for field work and harvesting activities.")
    elif 'cloud' in description:
        advice.append("☁️ Cloudy conditions: Good for transplanting as plants face less stress.")
    
    return advice if advice else ["🌾 Normal conditions: Continue with regular farming activities."]

def get_weather_icon_url(icon_code):
    """Get weather icon URL from OpenWeatherMap"""
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
