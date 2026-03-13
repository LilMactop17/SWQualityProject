# Step 1: Build the Rust Data Broker
FROM rust:1.75-slim as builder
WORKDIR /app
COPY databroker/Cargo.* ./databroker/
COPY databroker/ ./databroker/
WORKDIR /app/databroker
RUN cargo build --release

# Step 2: Set up the Python Runtime Environment
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies (needed for some networking/python libs)
RUN apt-get update && apt-get install -y libssl-dev ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy the Rust binary from the builder stage
COPY --from=builder /app/databroker/target/release/databroker /usr/local/bin/databroker

# Copy the Python adapters and JSON configs
COPY databroker/kuksa-ditto/ /app/kuksa-ditto/
RUN pip install --no-cache-dir -r kuksa-ditto/requirements.txt || true

# Copy your configuration files
COPY databroker/OBD.json /app/config/OBD.json

# Expose common ports for Zenoh/Kuksa/Ditto (Adjust if your config uses different ones)
EXPOSE 1883 8080 7447

# Start the Data Broker by default
# Note: You may need a shell script if you want to run the python adapters simultaneously
CMD ["databroker"]