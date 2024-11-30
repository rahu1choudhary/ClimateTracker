from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
REDIS_URL = "redis://:mypassword@host.docker.internal:6379/0"
redis_client = redis.from_url(REDIS_URL)

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
        
        # Convert byte data to strings if needed
        data = {k: float(v) if v else v for k, v in data.items()}
        return jsonify(data)

    except redis.RedisError as e:
        return jsonify({"error": f"Redis error: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
