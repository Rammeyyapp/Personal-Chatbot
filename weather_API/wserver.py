# server.py (Flask application)
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = "5992c7cc30d01b35ed1e422f4364428c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

def get_weather_data(city_name):
    """Fetches current weather data from OpenWeatherMap API."""
    if not API_KEY:
        return {"error": "API Key not configured on the server."}, 500

    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        # Check for city not found error from the API
        if data.get("cod") == "404":
            return {"error": f"City/Area '{city_name}' not found."}, 404

        # Extract relevant weather details
        weather_info = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature_c": data.get("main", {}).get("temp"),
            "feels_like_c": data.get("main", {}).get("feels_like"),
            "humidity_percent": data.get("main", {}).get("humidity"),
            "condition": data.get("weather", [{}])[0].get("main"),
            "description": data.get("weather", [{}])[0].get("description").title(),
            "wind_speed_m_s": data.get("wind", {}).get("speed")
        }
        return weather_info, 200

    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}"}, 500
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}, 500
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}, 500
    except Exception as e:
        return {"error": f"An unknown error occurred: {e}"}, 500


@app.route('/weather', methods=['GET'])
def weather_endpoint():
    """API endpoint to handle weather requests."""
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    weather_data, status_code = get_weather_data(city)
    return jsonify(weather_data), status_code

if __name__ == '__main__':
    print("Starting Flask server...")
    # The 'host='0.0.0.0'' makes the server externally accessible on the network
    app.run(host='127.0.0.1', port=5000, debug=True)