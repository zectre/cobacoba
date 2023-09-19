from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory storage for the latest location in raw data form
raw_location_data = []

# Function to convert raw data to GeoJSON format
# Function to convert raw data to GeoJSON format
def convert_to_geojson(raw_data):
    if raw_data:
        latest_data = raw_data[-1]  # Select the last data point from the list
        geojson_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(latest_data['Longitude']), float(latest_data['Latitude'])],
            },
            "properties": {
                "accuracy": float(latest_data['Accuracy']),
                "devicename": latest_data['Devicenm'],
            },
        }
        return {
            "type": "FeatureCollection",
            "features": [geojson_feature],
        }
    else:
        return None


@app.route('/log', methods=['POST'])
def log_location():
    data = request.json

    # Append the raw data to the list
    raw_location_data.append(data)

    # Broadcast the updated raw data to clients
    socketio.emit('location_update', data)  # Broadcast location update to clients

    return jsonify({'message': 'Location data received'}), 200

@app.route('/location', methods=['GET'])
def get_location():
    # Retrieve the raw data
    return jsonify(raw_location_data), 200

@app.route('/location_geojson', methods=['GET'])
def get_location_geojson():
    # Convert the raw data to GeoJSON format
    geojson_data = convert_to_geojson(raw_location_data)
    return jsonify(geojson_data), 200

@app.route('/show_location', methods=['GET'])
def show_location():
    # Convert the raw data to GeoJSON format for rendering in the template
    geojson_data = convert_to_geojson(raw_location_data)
    return render_template('index.html', location=geojson_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)