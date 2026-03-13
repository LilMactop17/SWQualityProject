# 1.
Run Docker Desktop
# 2.
Open a new command prompt
cd into the databroker folder
Run
```docker run -it --rm -p 55555:55555 -v "%cd%/OBD.json:/OBD.json" ghcr.io/eclipse-kuksa/kuksa-databroker:main --metadata /OBD.json```
# 3.
## Ensure you have C++ 14.0 or greater, along with a C++ compiler to install the requirements
Open a new command prompt
cd into the kuksa-ditto folder
Initialize the Virutal Environment using
```
python -m venv venv
```
Install the necessary Libraries using
```
pip install -r requirements.txt
```
Activate the virutal environment using
```
venv\Scripts\activate
```
Run
```
python send_obd_data_to_kuksa.py
```
Keep this window running
# 4.
Open a new command prompt
cd into the kuksa-ditto folder
Activate the virutal environment using
```
venv\Scripts\activate
```
Run
```
python kuksa_to_zenoh.py
```
Keep this window running
# 5.
Open a new command prompt
cd into the kuksa-ditto folder
Activate the virutal environment using
```
venv\Scripts\activate
```
Run
```
python zenoh_to_ditto.py



git clone https://github.com/LilMactop17/SWQualityProject.git
cd SWQualityProject

docker build -t sw-quality-app .

docker run -p 8080:8080 --name sw-project-instance sw-quality-app
```
Keep this window running
