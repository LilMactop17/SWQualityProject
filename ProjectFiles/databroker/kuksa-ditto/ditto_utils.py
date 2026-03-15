import requests

THINGS_URL = "http://ditto-gateway:8080/api/2"
DITTO_AUTH = ("ditto", "ditto")
THING_ID = "org.ovin:my-vehicle"
class DittoClient:
    def __init__(self, base_url, auth):
        self.things_url = f"{base_url}/things/"
        self.policies_url = f"{base_url}/policies/"
        self.auth = auth

    def get_thing(self, thing_id):
        response = requests.get(f"{self.things_url}{thing_id}", auth=self.auth)
        return response.json() if response.status_code == 200 else None

    def put_thing(self, thing_id, thing_data, force=False):
        url = f"{self.things_url}{thing_id}"
        if not force and self.get_thing(thing_id):
            answer = input(f"Thing {thing_id} exists. Overwrite? (y/n): ")
            if answer.lower() != 'y':
                return None

        return requests.put(url, json=thing_data, auth=self.auth)

    def update_property(self, thing_id, feature, property_path, value):
        """
        Versatile function to update any property inside a feature.
        Matches the path style: features/{feature}/properties/{property_path}
        """
        url = f"{self.things_url}{thing_id}/features/{feature}/properties/{property_path}"
        headers = {"Content-Type": "application/json"}
        # If value is a simple number/string, Ditto expects it as raw JSON value
        response = requests.put(url, json=value, headers=headers, auth=self.auth)
        return response

    # Add your other delete/policy functions here using 'self.auth' and 'self.policies_url'