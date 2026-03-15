from ditto_utils import DittoClient, THING_ID, THINGS_URL, DITTO_AUTH
import zenoh
import requests
import json

client = DittoClient(THINGS_URL, DITTO_AUTH)
setup_url = "http://localhost:8080/api/2/things/org.ovin:my-vehicle"
thingsURL = "http://localhost:8080/api/2/things/"
policiesURL = "http://localhost:8080/api/2/policies/"
auth = ("ditto" , "ditto")

# thing_skeleton = {
#     "policyId": "org.ovin:policy", # Make sure this policy exists or use 'default'
#     "features": {
#         "obd": {
#             "properties": {
#                 "VehicleSpeed": 0,
#                 "EngineSpeed": 0,
#                 "ThrottlePosition": 0,
#                 "CoolantTemperature": 0
#             }
#         }
#     }
# }
#
# print("Creating Digital Twin skeleton in Ditto...")
# response = requests.put(setup_url, json=thing_skeleton, auth=auth)
#
# if response.status_code in [201, 204]:
#     print("Success! The Digital Twin is ready to receive Zenoh data.")
# else:
#     print(f"Error creating Thing: {response.status_code} - {response.text}")

# policy_id = "org.ovin:policy"
# url = f"http://localhost:8080/api/2/policies/{policy_id}"
# auth = ("ditto", "ditto")

# This policy gives the 'ditto' user full READ and WRITE access
# policy_data = {
#     "entries": {
#         "owner": {
#             "subjects": {
#                 "nginx:ditto": {
#                     "type": "pre-authenticated"
#                 }
#             },
#             "resources": {
#                 "thing:/": {
#                     "grant": [
#                         "READ",
#                         "WRITE"
#                     ],
#                     "revoke": []
#                 },
#                 "policy:/": {
#                     "grant": [
#                         "READ",
#                         "WRITE"
#                     ],
#                     "revoke": []
#                 }
#             }
#         }
#     }
# }

# response = requests.put(url, json=policy_data, auth=auth)
# print(f"Policy Update Status: {response.status_code}")


def get_thing(thingID):
    url = thingsURL + thingID
    response = requests.get(url, auth=auth)
    return response.json() if response.status_code == 200 else None


def put_thing(thingID, ThingData):
    thing = get_thing(thingID)
    url = thingsURL + thingID
    if thing is None:
        headers = {"Content-Type": "Application/json"}
        response = requests.put(url, json=ThingData, headers=headers, auth=auth)
        return response
    else:
        print("There is a thing already created with the same thingID")
        print("Do you want to overwrite it (y/n)?")
        answer = input()
        if answer.lower() == 'y':
            headers = {"Content-Type": "Application/json"}
            response = requests.put(url, json=ThingData, headers=headers, auth=auth)
            return response


def patch_thing(thingID, ThingData):
    url = thingsURL + thingID
    headers = {"Content-Type": "Application/merge-patch+json"}
    response = requests.patch(url, json=ThingData, headers=headers, auth=auth)
    return response



def delete_thing(thingID):
    url = thingsURL + thingID
    response = requests.delete(url, auth=auth)
    return response


def put_policy(policyID, PolicyData):
    url = policiesURL + policyID
    headers = {"Content-Type": "Application/json"}
    response = requests.put(url, json=PolicyData, headers=headers, auth=auth)

    # Check if there is actually content to parse
    if response.status_code in [201, 204]:
        print(f"Policy '{policyID}' successfully updated (Status: {response.status_code}).")
        return {"status": "success", "code": response.status_code}
    else:
        # If there's an error, it might have a JSON error message
        try:
            return response.json()
        except:
            return response.text


def delete_policy(policyID):
    url = policiesURL + policyID
    response = requests.delete(url, auth=auth)
    if response.status_code == 204:
        print(f"Policy '{policyID}' successfully deleted.")
    else:
        print(f"Failed to delete policy '{policyID}'. Status code: {response.status_code}, Response: {response.text}")
    return response




def get_feature_value(thingID, feature):
    url = thingsURL + thingID + "/features/" + feature + "/properties/value"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        value = float(response.json())
        return value
    else:
        return response



def put_feature_value(thingID, feature, property_name, value):
    # Updated to point to the specific property name for exact capitalization
    url = f"{thingsURL}{thingID}/features/{feature}/properties/{property_name}"
    headers = {"Content-Type": "application/json"}
    # Passing value directly as a JSON float/number
    response = requests.put(url, json=value, headers=headers, auth=auth)
    return response

def handle_zenoh_update(sample):
    full_path = str(sample.key_expr)
    prop_name = full_path.split('/')[-1]

    try:
        value = float(sample.payload.to_string())
        response = put_feature_value(THING_ID, "obd", prop_name, value)

        print(f"Zenoh -> Ditto | {prop_name}: {value} | Status: {response.status_code}")

    except ValueError:
        print(f"Non-numeric data ignored on path: {full_path}")
    except Exception as e:
        print(f"Bridge Error: {e}")

conf = zenoh.Config()
conf.insert_json5("connect/endpoints", '["tcp/127.0.0.1:7447"]')

with zenoh.open(conf) as z_session:
    print(f"Subscribing to Zenoh and forwarding to Ditto ({THING_ID})...")
    sub = z_session.declare_subscriber("Vehicle/OBD/**", handle_zenoh_update)
    input("Press Enter to stop the bridge and exit...\n")