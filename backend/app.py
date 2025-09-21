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

# Creating Dataframe
df = pd.read_csv('StopsInfo.csv')
liverpool_active_df = df[(df["LocalityName"] == "Liverpool") & (df["Status"] == "active")]
location_df = liverpool_active_df[["Latitude", "Longitude"]]

# Combining longitude and Latitude into a single array for easier processing
location_data = []
for index,row in location_df.iterrows():
    try:
        location_data.append({'lat': float(row['Latitude']), 'lng': float(row['Longitude'])})
    except ValueError as e:
        location_data.append({'lat': 0, 'lng': 0}) # Deals with invalid locations

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

add_location()
print(updated_df)



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


def add_stops_to_df():
    # Will add a list of buses to a give stop ID
    for index, row in updated_df.iterrows():
        stop_id = row['NaptanCode']
        for stop in stops_with_buses:
            if stop['id'] == stop_id:
                updated_df.at[index, "Arriva"] = stop["buses"]["arriva"]
                updated_df.at[index, "Stagecoach"] = stop["buses"]["stagecoach"]
                
add_stops_to_df()


# Creating a dataframe consisting of only stops that have buses assigned to them
complete_df = updated_df[(updated_df["Arriva"] != "default") & (updated_df["Stagecoach"] != "default")] 


@app.route('/api/bus-stops', methods=['GET'])
def get_bus_stops():
    bus_stop_data = complete_df.to_json(orient="records")
    return bus_stop_data


bus_info = []
def fetch_data(company_name, company_id):
    api_url = f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/{company_id}/?api_key={api_key}"
    response = requests.get(api_url)
    with open(f"{company_name}_liverpool.txt", "w", encoding='utf-8') as f:
        f.write(response.text) 


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

    if bus_company == "stagecoach":
        company_id = 1695
    elif bus_company == "arriva":
        company_id = 709

    fetch_data(bus_company, company_id)

    # XML structure example:
    # Siri -> ServiceDelivery -> VehicleMonitoringDelivery -> VehicleActivity (Where the data about individual buses live)
    # Parse through data and extract requested buses
    tree = ET.parse(f'{bus_company}_liverpool.txt')
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
                    long = location.find('./siri:Longitude', ns)
                    bus_info.append({'lat':float(lat.text), 'lng':float(long.text)})

    return jsonify({
        "message": "Got the bus",
        "buses":bus_info,
    })


if __name__ == '__main__':
    app.run()
