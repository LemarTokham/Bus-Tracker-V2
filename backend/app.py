from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

bus_stops = [
    {'name': 'Brownlow Hill',
     'id':'merdjapg',
     'buses':[76, 201, 699],
     'location': {'lat': 53.4055, 'lng': -2.9618 } # [Lat, Long]
     },
     {'name': 'Crown Street',
     'id':'merdjapd',
     'buses':[201, 6, 7, 79],
     'location': {'lat': 53.4061, 'lng': -2.96366 }
     }
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "FLask is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/bus-stops', methods=['GET'])
def get_bus_stops():
    return jsonify({
        "bus_stops":bus_stops
    })


if __name__ == '__main__':
    app.run(debug=True)
