from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

CORS(app)

weather_data = [
    {"place": "Alappuzha", "date": datetime.now().strftime("%a %H:%M"), "temperature": "26°C"},
    {"place": "Kollam", "date": datetime.now().strftime("%a %H:%M"), "temperature": "24°C"},
    {"place": "Thiruvananthapuram", "date": datetime.now().strftime("%a %H:%M"), "temperature": "32°C"},
    {"place": "Kochi", "date": datetime.now().strftime("%a %H:%M"), "temperature": "26°C"},
    {"place": "Kottayam", "date": datetime.now().strftime("%a %H:%M"), "temperature": "25°C"}
]

@app.route('/weather', methods=['GET'])
def get_weather():
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
