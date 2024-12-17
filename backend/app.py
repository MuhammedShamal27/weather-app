from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

CORS(app)


# Weather data (can be replaced with dynamic data in the future)
weather_data = [
    {"place": "Alappuzha", "date": datetime.now().strftime("%a %H:%M"), "temperature": "26°C"},
    {"place": "Kollam", "date": datetime.now().strftime("%a %H:%M"), "temperature": "24°C"},
    {"place": "Thiruvananthapuram", "date": datetime.now().strftime("%a %H:%M"), "temperature": "32°C"},
    {"place": "Kochi", "date": datetime.now().strftime("%a %H:%M"), "temperature": "26°C"},
    {"place": "Kottayam", "date": datetime.now().strftime("%a %H:%M"), "temperature": "25°C"}
]

# Route to return weather data as JSON
@app.route('/weather', methods=['GET'])
def get_weather():
    return jsonify(weather_data)

# Run the server
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000)
