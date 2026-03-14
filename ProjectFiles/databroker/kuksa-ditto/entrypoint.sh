#!/bin/sh

# 1. Start the Rust Databroker in the background
# We use & to let the script keep running
databroker --address 0.0.0.0 --port 55555 &

# Give the broker 3 seconds to fully initialize
sleep 3

# 2. Start the 4 Python scripts in the background
echo "Starting Python adapters..."
python3 /app/kuksa-ditto/send_obd_data_to_kuksa.py &
python3 /app/kuksa-ditto/kuksa_to_zenoh.py &
python3 /app/kuksa-ditto/zenoh_to_ditto.py &
python3 /app/kuksa-ditto/sovd-server.py &

# 3. Wait indefinitely so the container doesn't exit
# This keeps the foreground process alive
wait