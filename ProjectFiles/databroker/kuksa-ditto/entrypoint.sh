#!/bin/sh

# 1. Start the Rust Databroker with the VSS configuration
# Adding --metadata is CRITICAL, otherwise you get the 404 error
databroker --address 0.0.0.0 --port 55555 --metadata /app/config/OBD.json &

# Give the broker 10 seconds to fully initialize
# Rust compilation/startup inside Docker can be slow
echo "Waiting 10s for Databroker..."
sleep 10

# 2. Start the Python scripts with 10s delays between each
# The -u flag ensures logs appear immediately in your terminal
echo "Starting Python adapters..."

echo "-> Launching: send_obd_data_to_kuksa.py"
python3 -u /app/kuksa-ditto/send_obd_data_to_kuksa.py &
sleep 10

echo "-> Launching: kuksa_to_zenoh.py"
python3 -u /app/kuksa-ditto/kuksa_to_zenoh.py &
sleep 10

echo "-> Launching: zenoh_to_ditto.py"
python3 -u /app/kuksa-ditto/zenoh_to_ditto.py &
sleep 10

echo "-> Launching: sovd-server.py"
python3 -u /app/kuksa-ditto/sovd-server.py &

# 3. Wait indefinitely
echo "All systems active. Monitoring output..."
wait