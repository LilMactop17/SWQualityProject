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