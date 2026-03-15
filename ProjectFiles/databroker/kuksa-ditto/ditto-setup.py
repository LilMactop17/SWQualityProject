from ditto_utils import DittoClient, THING_ID, THINGS_URL, DITTO_AUTH
import zenoh
import requests
import json
import time

client = DittoClient(THINGS_URL, DITTO_AUTH)
setup_url = "http://localhost:8080/api/2/things/org.ovin:my-vehicle"
thingsURL = "http://localhost:8080/api/2/things/"
policiesURL = "http://localhosty:8080/api/2/policies/"
auth = ("ditto" , "ditto")

thing_skeleton = {
    "policyId": "org.ovin:policy", # Make sure this policy exists or use 'default'
    "features": {
        "obd": {
            "properties": {
                "VehicleSpeed": 0,
                "EngineSpeed": 0,
                "ThrottlePosition": 0,
                "CoolantTemperature": 0
            }
        }
    }
}

print("Creating Digital Twin skeleton in Ditto...")
response = requests.put(setup_url, json=thing_skeleton, auth=auth)

if response.status_code in [201, 204]:
    print("Success! The Digital Twin is ready to receive Zenoh data.")
else:
    print(f"Error creating Thing: {response.status_code} - {response.text}")

policy_id = "org.ovin:policy"
url = f"http://localhost:8080/api/2/policies/{policy_id}"
auth = ("ditto", "ditto")

# This policy gives the 'ditto' user full READ and WRITE access
policy_data = {
    "entries": {
        "owner": {
            "subjects": {
                "nginx:ditto": {
                    "type": "pre-authenticated"
                }
            },
            "resources": {
                "thing:/": {
                    "grant": [
                        "READ",
                        "WRITE"
                    ],
                    "revoke": []
                },
                "policy:/": {
                    "grant": [
                        "READ",
                        "WRITE"
                    ],
                    "revoke": []
                }
            }
        }
    }
}

def wait_for_ditto():
    print("Waiting for Ditto Gateway to wake up...")
    while True:
        try:
            # Check if the gateway is responding
            r = requests.get("http://localhost:8080/health", timeout=2)
            break
        except:
            print("Ditto is still booting... sleeping 5s")
            time.sleep(5)

wait_for_ditto()

# STEP 1: Create Policy FIRST
print(f"Creating Policy: {policy_id}...")
policy_response = requests.put(url, json=policy_data, auth=auth)
print(f"Policy Status: {policy_response.status_code}")

# STEP 2: Create Thing SECOND
print("Creating Digital Twin skeleton...")
thing_response = requests.put(setup_url, json=thing_skeleton, auth=auth)
print(f"Thing Status: {thing_response.status_code}")