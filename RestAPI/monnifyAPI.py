import os
import requests
import base64
import json
from Dashboard.models import WebsiteConfiguration

# Your input string
input_string = os.getenv("MONNIFY_AUTH_TOKEN2", "")

# Convert string to bytes
input_bytes = input_string.encode('utf-8')

# Encode the bytes to Base64
base64_bytes = base64.b64encode(input_bytes)

# Convert Base64 bytes back to string for display
base64_string = base64_bytes.decode('utf-8')

# print("Base64 Encoded:", base64_string)


class MonnifyAPI:
    def __init__(self, base_url=None, auth_token=None):
        # Retrieve the base_url and auth_token from the WebsiteConfiguration model
        base_url, auth_token = WebsiteConfiguration.get_configuration()
        if not base_url or not auth_token:
            raise ValueError("API configuration is not set in the database.")
        
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

    def login(self):
        url = f"{self.base_url}/api/v1/auth/login"
        headers = {
            "Authorization": f"Basic {base64_string}",  
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers)
        print("Login POST URL: " + url)
        print("Actual status code:", response.status_code)
        print("Response content:", response.content)

        try:
            json_data = response.json()
            json_str = json.dumps(json_data, indent=4)
            print("JSON Login response body: ", json_str)
            if response.status_code == 200:
                print("Login successful.")
                # Extract token if the login was successful
                self.auth_token = json_data.get("access_token")  # Adjust according to API response
                if self.auth_token:
                    self.headers["Authorization"] = f"Bearer {self.auth_token}"
                    return json_data
                else:
                    print("Access token not found in response.")
            else:
                print("Login failed with status code:", response.status_code)
                return None
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)

        return None

    def get_account_details(self, data):
        if not self.auth_token:
            print("Error: No valid auth_token. Please log in first.")
            return None
        
        url = f"{self.base_url}/api/v2/bank-transfer/reserved-accounts"
        print("POST URL: " + url)
        
        response = requests.post(url, json=data, headers=self.headers)
        print("Actual status code:", response.status_code)
        print("Response content:", response.content)

        try:
            json_data = response.json()
            json_str = json.dumps(json_data, indent=4)
            print("JSON POST response body: ", json_str)
            user_id = json_data.get("id")
            print("User ID ===>", user_id)
            print(".......POST/DATA TopUp Is Done.......")
            print(".......=====================.......")
            return user_id
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)

        return None
