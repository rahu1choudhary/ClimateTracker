from flask import Flask, request, jsonify
import requests
import redis

app = Flask(__name__)

# Kestra API details
KESRA_API_URL = 'http://localhost:8080/api/workflows/fetch-weather-workflow'
KESRA_API_TOKEN = 'your-kestra-api-token'  # Replace with your actual Kestra API token

# Redis configuration
REDIS_URL = "redis://:mypassword@host.docker.internal:6379/0"
redis_client = redis.from_url(REDIS_URL)

@app.route('/trigger-kestra-workflow', methods=['POST'])
def trigger_kestra_workflow():
    data = request.get_json()
    city = data.get('city')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    headers = {
        'Authorization': f'Bearer {KESRA_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        'inputs': {
            'city': city
        }
    }

    # Trigger the Kestra workflow
    response = requests.post(KESRA_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return jsonify({'message': 'Workflow triggered successfully'}), 200
    else:
        return jsonify({'error': response.text}), response.status_code

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        # Retrieve data from Redis
        data = {
            "temperature_c": redis_client.get(f"weather:{city}:temperature_c"),
            "temperature_f": redis_client.get(f"weather:{city}:temperature_f"),
            "humidity": redis_client.get(f"weather:{city}:humidity"),
            "wind_speed_kph": redis_client.get(f"weather:{city}:wind_speed_kph"),
            "cloud": redis_client.get(f"weather:{city}:cloud")
        }
        
        if any(value is None for value in data.values()):
            return jsonify({"error": "Data not found for the given city"}), 404
        
        # Convert byte data to strings or floats as needed
        data = {k: float(v) if v else v for k, v in data.items()}
        return jsonify(data)

    except redis.RedisError as e:
        return jsonify({"error": f"Redis error: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
