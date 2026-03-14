# ---------- Stage 1: Rust builder ----------
FROM rust:1.82-slim AS builder

RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl3 \
    protobuf-compiler \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/ProjectFiles

# Copy manifest files first for better caching
COPY ProjectFiles/Cargo.toml ProjectFiles/Cargo.lock ./
COPY ProjectFiles/databroker/Cargo.toml ./databroker/
COPY ProjectFiles/databroker-proto/Cargo.toml ./databroker-proto/

# If you have other workspace crates, copy their Cargo.toml files too
# COPY ProjectFiles/other-crate/Cargo.toml ./other-crate/

# Create dummy source files so cargo can build dependencies
RUN mkdir -p databroker/src databroker-proto/src && \
    printf 'fn main() {}\n' > databroker/src/main.rs && \
    printf 'pub fn dummy() {}\n' > databroker-proto/src/lib.rs

# Build dependencies only
RUN cargo build --release --package databroker || true

# Now copy the real source code
COPY ProjectFiles ./

# Build with actual sources
RUN cargo build --release --package databroker


# ---------- Stage 2: Python runtime ----------
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libssl-dev \
    ca-certificates \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/ProjectFiles/target/release/databroker /usr/local/bin/databroker

COPY ProjectFiles/databroker/kuksa-ditto /app/kuksa-ditto/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    kuksa-client==0.4.1 \
    eclipse-zenoh \
    paho-mqtt \
    flask \
    requests

RUN mkdir -p /app/config
COPY ProjectFiles/databroker/OBD.json /app/config/OBD.json

COPY ProjectFiles/databroker/kuksa-ditto/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 1883 8080 7447 55555

ENTRYPOINT ["entrypoint.sh"]