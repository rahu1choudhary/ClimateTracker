import sys
import requests
import json
import redis

# Function to connect to Redis using a URL
def connect_to_redis(url="redis://:mypassword@host.docker.internal:6379/0"):
    try:
        r = redis.from_url(url)
        r.ping()  # Test the connection
        print("Connected to Redis via URL")
        return r
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        return None
    except redis.AuthenticationError as e:
        print(f"Redis authentication failed: {e}")
        return None

# Function to fetch weather data and store it in Redis
def fetch_and_store_weather(api_key, city, redis_client):
    try:
        # Construct API URL
        api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

        # Make the API request
        response = requests.get(api_url)
        if response.status_code == 200:
            weather_data = response.json()
            print("Weather Data:", json.dumps(weather_data, indent=4))

            # Filter required fields
            current_weather = weather_data.get("current", {})
            filtered_data = {
                "temperature_c": current_weather.get("temp_c"),
                "temperature_f": current_weather.get("temp_f"),
                "humidity": current_weather.get("humidity"),
                "wind_speed_kph": current_weather.get("wind_kph"),
                "cloud": current_weather.get("cloud"),
            }

            # Store all attributes under a single hash key in Redis
            redis_key = f"weather:{city}"
            redis_client.hset(redis_key, mapping=filtered_data)
            print(f"Weather data for {city} stored in Redis under key: {redis_key}")

        else:
            print(f"Failed to fetch weather data. Status Code: {response.status_code}")
            print("Error Message:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")
    except redis.RedisError as e:
        print(f"An error occurred while interacting with Redis: {e}")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_weather.py <city_name>")
        sys.exit(1)

    city = sys.argv[1]
    API_KEY = "5112a95172c9498d9e294254243011"
    REDIS_URL = "redis://:mypassword@host.docker.internal:6379/0"

    redis_client = connect_to_redis(REDIS_URL)
    if redis_client:
        fetch_and_store_weather(API_KEY, city, redis_client)
