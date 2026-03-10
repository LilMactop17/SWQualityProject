docker run -it --rm -p 55555:55555 -v "%cd%/OBD.json:/OBD.json" ghcr.io/eclipse-kuksa/kuksa-databroker:main --metadata /OBD.json
