from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

bus_stops = [
    {'name': 'Brownlow Hill',
     'id':'merdjapg',
     'Buses':[76, 201, 699],
     'Location': [-2.9618, 53.4055] # Long and Lat
     },
     {'name': 'Crown Street',
     'id':'merdjapd',
     'Buses':[201, 6, 7, 79],
     'Location': [-2.96366, 53.4061]
     }
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "FLask is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


if __name__ == '__main__':
    app.run(debug=True)
