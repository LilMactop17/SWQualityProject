# 1.
Run Docker Desktop
# 2.
Open a new command prompt
cd into the databroker folder
Run
```docker run -it --rm -p 55555:55555 -v "%cd%/OBD.json:/OBD.json" ghcr.io/eclipse-kuksa/kuksa-databroker:main --metadata /OBD.json```
# 3.
Open a new command prompt
cd into the kuksa-ditto folder
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
```
Keep this window running
