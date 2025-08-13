from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json
import xml.etree.ElementTree as ET
import threading
from flask_socketio import SocketIO, send, emit, join_room, leave_room

# Load api key
load_dotenv()
api_key = os.getenv('API_KEY')

# Define app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,cors_allowed_origins="*")



bus_stops = [
    {'name': 'Brownlow Hill',
     'id':'merdjapg',
     'buses':["76", "201", "699"],
     'location': {'lat': 53.40575, 'lng': -2.9618 } # [Lat, Long]
     },
     {'name': 'Crown Street',
     'id':'merdjapd',
     'buses':["201", "6", "7", "79"],
     'location': {'lat': 53.40611, 'lng': -2.96367 }
     },
    {'name': 'Shaw Street',
     'id':'merdgwtp', # TODO: put in indicator field to distinguish between buses on same street
     'buses':["14", "14A", "14B", "14X", "17", "17A", "17X", "19"], # TODO: Differentiate between arriva and stagecoach buses
     'location': {'lat': 53.41204, 'lng': -2.96723}
     }
]


# Download the XML, parse through it for all relevant bus, send data off to API, repeat every 10 seconds
def fetch_data():
    api_url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/1695/?api_key={api_key}"
    response = requests.get(api_url)
    print(response.encoding)
    with open("stagecoach_liverpool.txt", "w", encoding='utf-8') as f:
        f.write(response.text) 

    threading.Timer(10, fetch_data).start() # Start a new thread where this function will be ran every 10 seconds

fetch_data() # Start first function cal


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
    bus_info = []
    bus_line = request.json
    print(f"Recived {bus_line}")
    # XML structure example:
    # Siri -> ServiceDelivery -> VehicleMonitoringDelivery -> VehicleActivity (Where the data about individual buses live)
    tree = ET.parse('stagecoach_liverpool.txt')
    ns = {'siri': "http://www.siri.org.uk/siri"}
    root = tree.getroot()
    allVehicles = root.findall('.//siri:VehicleActivity', ns)
    for vehicle in allVehicles:
        journey = vehicle.find('./siri:MonitoredVehicleJourney', ns)
        if journey is not None: # Checking for a tracked journey
            bus = journey.find('./siri:LineRef', ns)
            if bus is not None and bus.text == bus_line: # Checking if a bus is being tracked
                location = journey.find('./siri:VehicleLocation', ns)
                if location is not None : # Checking if we have both longitude and latitude
                    lat = location.find('./siri:Latitude', ns)
                    long = location.find('./siri:Longitude', ns)
                    bus_info.append({'lat':float(lat.text), 'lng':float(long.text)})

    return jsonify({
        "message": "Got the bus",
        "buses":bus_info
    })


# Web Socket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(msg):
    print(f'Recieved message: {msg}')
    send(f'Echo: {msg}') # Send it back to client



if __name__ == '__main__':
    socketio.run(app)
