from flask import Flask, jsonify
from kuksa_client.grpc import VSSClient

app = Flask(__name__)

KUKSA_IP = "127.0.0.1"
KUKSA_PORT = 55555
@app.route('/')
def home():
    return """
    <h1>OpenSOVD Gateway Online</h1><p>Try: <a href='/v1/diagnostic-data/VehicleSpeed'>Vehicle Speed</a></p>
    </ br><p>Try: <a href='/v1/diagnostic-data/EngineSpeed'>Engine Speed</a></p>
    </ br><p>Try: <a href='/v1/diagnostic-data/ThrottlePosition'>Throttle Position</a></p>
    </ br><p>Try: <a href='/v1/diagnostic-data/CoolantTemperature'>Coolant Temperature</a></p>
    """
def get_vss_value(path):
    try:
        with VSSClient(KUKSA_IP, KUKSA_PORT) as client:
            updates = client.get_current_values([path])
            if path in updates and updates[path] is not None:
                return updates[path].value
            return None
    except Exception as e:
        print(f"Kuksa Connection Error: {e}")
        return None

@app.route('/')
def nothome():
    return "OpenSOVD Gateway is Running. Use /v1/diagnostic-data/VehicleSpeed"

@app.route('/v1/diagnostic-data/<signal_id>', methods=['GET'])
def get_diagnostic_data(signal_id):
    # This preserves your exact capitalization
    vss_path = f"Vehicle.OBD.{signal_id}"
    print(f"SOVD Request for: {signal_id} -> Querying Kuksa: {vss_path}")
    
    value = get_vss_value(vss_path)
    
    if value is None:
        print(f"Error: {vss_path} not found in Kuksa!")
        return jsonify({"error": f"Resource {signal_id} not found"}), 404

    return jsonify({
        "links": {"self": f"/v1/diagnostic-data/{signal_id}"},
        "data": {
            "id": signal_id,
            "value": value,
            "unit": "standard"
        }
    })

if __name__ == "__main__":
    app.run(port=8081, debug=True)