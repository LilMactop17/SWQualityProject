# Step 1: Build the Rust Data Broker
FROM rust:1.82-slim AS builder

# Install system dependencies required for compilation
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    protobuf-compiler \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Copy everything (including the Project/ folder)
COPY . .

# 2. Move into the actual project root where Cargo.toml lives
WORKDIR /app/ProjectFiles

# 3. THE PROTO FIX: 
# Pointing specifically to the internal proto directory so 'sdv/...' 
# imports resolve correctly relative to /app/Project/proto
ENV PROTOC_INCLUDE=/app/ProjectFiles/databroker-proto
ENV PROTOC_ARGS="-I /app/ProjectFiles/databroker-proto"

# 4. Build the release binary
# This handles the heavy lifting of compiling Tonic, Tokio, etc.
RUN cargo build --release --package databroker

# --- Step 2: Set up the Python Runtime Environment ---
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y libssl-dev ca-certificates && rm -rf /var/lib/apt/lists/*

# 1. Copy the Rust binary (This path is correct based on Stage 1)
COPY --from=builder /app/ProjectFiles/target/release/databroker /usr/local/bin/databroker

# 2. THE FIX: Copying the Python files. 
# Using a wildcard or a more direct path to ensure we hit the folder
COPY ProjectFiles/databroker/kuksa-ditto /app/kuksa-ditto/

# 3. Install requirements
RUN if [ -f /app/kuksa-ditto/requirements.txt ]; then \
    pip install --no-cache-dir -r /app/kuksa-ditto/requirements.txt; \
    fi

# 4. Copy configuration
RUN mkdir -p /app/config
# Using a wildcard match to avoid case-sensitivity or pathing "not found" errors
COPY ProjectFiles/databroker/OBD.json /app/config/OBD.json

EXPOSE 1883 8080 7447
CMD ["databroker"]