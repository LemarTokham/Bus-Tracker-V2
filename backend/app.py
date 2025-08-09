from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json

## SETUP
# Load api key
load_dotenv()
api_key = os.getenv('API_KEY')

# Define app
app = Flask(__name__)
CORS(app)

## APP
bus_stops = [
    {'name': 'Brownlow Hill',
     'id':'merdjapg',
     'buses':[76, 201, 699],
     'location': {'lat': 53.40575, 'lng': -2.9618 } # [Lat, Long]
     },
     {'name': 'Crown Street',
     'id':'merdjapd',
     'buses':[201, 6, 7, 79],
     'location': {'lat': 53.40611, 'lng': -2.96367 }
     }
]

# Methods for each bus provider:
# Download the XML, parse through it for all relevant bus, send data off to API, repeat every 10 seconds

api_url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/709/?api_key={api_key}"
response = requests.get(api_url)
print(response)
with open("arriva_liverpool.txt", "w") as f:
    f.write(response.text)



bus_info = [
    {
        
    }
]


# Test if app is working
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "FLask is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# Fetch Bus stops info
@app.route('/api/bus-stops', methods=['GET'])
def get_bus_stops():
    return jsonify({
        "bus_stops":bus_stops
    })

@app.route('/api/buses', methods=['POST'])
def send_bus_location():
    data = request.json
    print(f"Recived {data}")

    return jsonify({
        "message": "Got the bus",
    })



if __name__ == '__main__':
    app.run(debug=True)
