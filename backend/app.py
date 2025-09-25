from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json
import xml.etree.ElementTree as ET
import time
import pandas as pd


# Setup
load_dotenv()
api_key = os.getenv('API_KEY')
app = Flask(__name__)
CORS(app)
COMPANY_IDS = {
    "stagecoach": 1695,
    "arriva": 709
}

# In-memory cache
last_bus_data = {} # Dicts for different bus companies
last_fetch_time = {}


# Creating Dataframe
df = pd.read_csv('StopsInfo.csv')

# Only want active stops within liverpool
liverpool_active_df = df[(df["LocalityName"] == "Liverpool") & (df["Status"] == "active")]

# Combining longitude and Latitude into a single array for easier processing
location_df = liverpool_active_df[["Latitude", "Longitude"]]
location_data = []
for index,row in location_df.iterrows():
    try:
        location_data.append({'lat': float(row['Latitude']), 'lng': float(row['Longitude'])})
    except ValueError as e:
        location_data.append({'lat': 0, 'lng': 0}) # Deals with invalid locations

# Filtering to include only the columns we want
updated_df = liverpool_active_df[["NaptanCode","CommonName","Street","Indicator", "LocalityName"]]

# Adding columns
updated_df["Arriva"] = "default"
updated_df["Stagecoach"] = "default"
updated_df['Location'] = "default"


def add_location():
    count = 0
    for index, row in updated_df.iterrows():
        updated_df.at[index, 'Location'] = location_data[count]
        count+=1

def add_stops_to_df():
    # Will add a list of buses to a give stop ID
    for index, row in updated_df.iterrows():
        stop_id = row['NaptanCode']
        for stop in stops_with_buses:
            if stop['id'] == stop_id:
                updated_df.at[index, "Arriva"] = stop["buses"]["arriva"]
                updated_df.at[index, "Stagecoach"] = stop["buses"]["stagecoach"]



# When adding a new bus stop with buses, it needs to be added here so the program can add it to the dataframe
stops_with_buses = [
    {
     'id':'merdjapg',
     'buses':{"arriva": ["76", "201", "699"],
              "stagecoach":[]},
     },
     {
     'id':'merdjapd',
     'buses':{"arriva": ["201", "6", "7", "79"],
              "stagecoach":[]},
     },
    {
     'id':'merdgwtp',
     'buses':{"arriva": [],
              "stagecoach":["17", "17A", "17X", "19", "19X", "14", "14A", "14B", "14X"]},
     },
]

# Running functions to build bus location dataframe 
add_location()           
add_stops_to_df()

# Creating a dataframe consisting of only stops that have buses assigned to them as those are the only ones the client needs
complete_df = updated_df[(updated_df["Arriva"] != "default") & (updated_df["Stagecoach"] != "default")] 


bus_info = []
def fetch_data(company_name, company_id):
    api_url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/{company_id}/?api_key={api_key}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return ET.ElementTree(ET.fromstring(response.text)) # Returns a ready-to-use tree
    except requests.RequestException as e:
        return None
    

def fetch_data_cached(company_name, company_id, ttl=10):
    now = time.time()

    # If we already have recently fetched data for a company, return cached data
    if company_name in last_bus_data and (now - last_fetch_time[company_name]) < ttl:
        return last_bus_data[company_name]
    
    # else get new data
    tree = fetch_data(company_name, company_id)
    if tree:
        last_bus_data[company_name] = tree
        last_fetch_time[company_name] = now
    return tree


# Endpoints
@app.route('/api/bus-stops', methods=['GET'])
def get_bus_stops():
    bus_stop_data = complete_df.to_json(orient="records")
    return bus_stop_data


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "FLask is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


@app.route('/api/buses', methods=['POST'])
def send_bus_location():
    bus_data = request.json

    bus_line = bus_data["busLine"]
    bus_company = bus_data["busCompany"]

    company_id = COMPANY_IDS.get(bus_company)
    if not company_id:
        return jsonify({"message": "Invalid bus company"}), 400 # Bad Request
    

    tree = fetch_data_cached(bus_company, company_id)
    if tree is None:
        return jsonify({"message": "Failed to fetch"}), 502 # Bad Gateway
    
    ns = {'siri': "http://www.siri.org.uk/siri"}
    root = tree.getroot()
    allVehicles = root.findall('.//siri:VehicleActivity', ns)

    bus_info = []
    for vehicle in allVehicles:
        journey = vehicle.find('./siri:MonitoredVehicleJourney', ns)
        if journey is not None: # Checking for a tracked journey
            bus = journey.find('./siri:LineRef', ns)
            if bus is not None and bus.text == bus_line: # Checking if a bus is being tracked
                location = journey.find('./siri:VehicleLocation', ns)
                if location is not None : # Checking if we have a location
                    lat = location.find('./siri:Latitude', ns)
                    lng = location.find('./siri:Longitude', ns)
                    bus_info.append({'lat':float(lat.text), 'lng':float(lng.text)})

    return jsonify({
        "message": "Got the bus",
        "buses":bus_info,
    })


if __name__ == '__main__':
    app.run()
