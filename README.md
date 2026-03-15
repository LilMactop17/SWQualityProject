# Assumes Docker and Docker Compose are installed on a Windows System

# 1: Run Eclipse Ditto
## Clone the repo
```
cd ~
git clone https://github.com/eclipse-ditto/ditto.git
```
## CD into the repo and run Ditto
```
cd ~/ditto/deployment/docker
docker compose up -d
```

# 2: Activate Databroker
## Clone this repo
```
cd ~
git clone https://github.com/LilMactop17/SWQualityProject.git SWQualityProject
```
## CD into the databroker folder and activate the databroker
```
cd ~/SWQualityProject/ProjectFiles/databroker
docker run --rm -it -p 55555:55555 -v "%cd%/OBD.json:/OBD.json" ghcr.io/eclipse-kuksa/kuksa-databroker:main --insecure --vss /OBD.json
```

# 3: Adjust Ditto Policies
## Open a new Command Prompt terminal
## CD into the kuksa-ditto folder
```
cd ~/SWQualityProject/ProjectFiles/databroker/kuksa-ditto
```
## Activate the virtual environment and install dependencies in the kuksa-ditto directory
```
venv\Scripts\activate
pip install -r requirements.txt
```
## Run ditto-setup.py to adjust policies
```
python ditto-setup.py
```

# 4: Generate Random Values for Kuks
## Open a new CMD terminal
## Cd into the kuksa-ditto folder and activate the virtual environment
```
cd ~/SWQualityProject/ProjectFiles/databroker/kuksa-ditto
venv\Scripts\activate
```
## Run send_obd_data_to_kuksa.py
```
python send_obd_data_to_kuksa.py
```
Keep this running in the background

# 5: Send Values to Zenoh
## Open a new CMD terminal
## Cd into the kuksa-ditto folder and activate the virtual environment
```
cd ~/SWQualityProject/ProjectFiles/databroker/kuksa-ditto
venv\Scripts\activate
```
## Run kuksa_to_zenoh.py
```
python kuksa_to_zenoh.py
```
Keep this running in the background

# 6: Send Zenoh Values to Ditto
## Open a new CMD terminal
## Cd into the kuksa-ditto folder and activate the virtual environment
```
cd ~/SWQualityProject/ProjectFiles/databroker/kuksa-ditto
venv\Scripts\activate
```
## Run zenoh_to_ditto.py
```
python zenoh_to_ditto.py
```
Keep this running in the background

# 7: Run OpenSOVD to allow REST API
## Open a new CMD terminal
## Cd into the kuksa-ditto folder and activate the virtual environment
```
cd ~/SWQualityProject/ProjectFiles/databroker/kuksa-ditto
venv\Scripts\activate
```
## Run sovd-server.py
```
python sovd-server.py
```
Keep this running in the background

# 7: Open Ditto
## Go to localhost:8080 and follow the steps to login

# 8: GET car values from OpenSOVD
## Go to localhost:8081
## Click on the links to get a specific car variable at that given moment