# client.py (Python script to interact with the server)
import requests

SERVER_URL = "http://127.0.0.1:5000/weather"

def get_weather_from_server(city_name):
    """Sends the city name to the server and prints the result."""
    print(f"\nRequesting weather for: {city_name}...")
    try:
        # Construct the full URL with the city parameter
        response = requests.get(SERVER_URL, params={'city': city_name})
        
        # Parse the JSON response
        data = response.json()

        if response.status_code == 200:
            # Successful response
            print("\n--- Current Weather Conditions ---")
            print(f"Area: {data['city']}, {data['country']}")
            print(f"Temperature: {data['temperature_c']} °C")
            print(f"Feels Like: {data['feels_like_c']} °C")
            print(f"Condition: {data['condition']} ({data['description']})")
            print(f"Humidity: {data['humidity_percent']}%")
            print(f"Wind Speed: {data['wind_speed_m_s']} m/s")
            print("----------------------------------")
        else:
            # Error response from the server
            error_message = data.get('error', 'Unknown Server Error')
            print(f"\n[ERROR] Could not fetch weather: {error_message}")
            print(f"Status Code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection failed. Is the server (server.py) running at 127.0.0.1:5000?")
    except Exception as e:
        print(f"\n[ERROR] An unexpected client error occurred: {e}")


if __name__ == '__main__':
    while True:
        area_input = input("Enter Area/District Name (or 'exit' to quit): ").strip()
        
        if area_input.lower() == 'exit':
            break
        if area_input:
            get_weather_from_server(area_input)
        else:
            print("Please enter a valid area name.")

    print("Client application closed.")