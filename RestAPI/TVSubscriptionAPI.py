import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime as Mdate
import random, uuid


# VTPassDataAPI class definition
class VTPassTVSubscription:
    def __init__(self, base_url, auth_token, secret_key):
        self.base_url = base_url
        self.auth_token = auth_token
        self.secret_key = secret_key
        self.headers = {
            "Authorization": self.auth_token,
            "Secret-Key": self.secret_key   
        }

    def verify_smartCard_number(self, data):
        url = "https://sandbox.vtpass.com/api/merchant-verify"
        print("Sending data to API:", data)
        
        # Sending POST request to the API
        response = requests.post(url, json=data, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)

        try:
            result = response.json()  # Directly parse the JSON response
            print("JSON POST response body: ", json.dumps(result, indent=4))
            return result  # Return the full response (not just transaction ID)
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)
            return None

    def bouquet_change(self, payload):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
        # Sending POST request to the API
        response = requests.post(url, json=payload, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)

        try:
            result = response.json()  # Directly parse the JSON response
            print("JSON POST response body: ", json.dumps(result, indent=4))
            return result  # Return the full response (not just transaction ID)
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)
            return None

    def fetch_service_variations(self, network_name):
        """
        Helper method to fetch service variations from the external API.
        """
        url = "https://sandbox.vtpass.com/api/service-variations?serviceID="
        payload = json.dumps({
            "serviceID": f"{network_name}"
        })
        headers = {
            'Authorization': '',
            'Content-Type': 'application/json',
        }

        # External GET request to retrieve service variations
        response = requests.get(url, headers=headers, data=payload)
        
        # Print the raw response for debugging purposes
        print(f"Service Variations for {network_name}: {response.text}")
        # print(f"Raw Response from fetch_service_variations: {response.text}")

        return response.text

# Helper function to create random ID
def create_random_id():
    num = random.randint(1000, 4999)
    num_2 = random.randint(5000, 8000)
    num_3 = random.randint(111, 999) * 2
    return str(num) + str(num_2) + str(num_3) + str(uuid.uuid4())

# Main program execution
if __name__ == "__main__":
    # URL and authentication details
    base_url = "https://sandbox.vtpass.com"
    auth_token = "Token be76014119dd44b12180ab93a92d63a2"
    secret_key = "SK_873dc5215f9063f6539ec2249c8268bb788b3150386"

    # Instantiate VTPassDataAPI object
    api = VTPassTVSubscription(base_url, auth_token, secret_key)

    data = {
        "billersCode": "7032148522",
        "serviceID": "gotv",
    }

    # Data for POST request
    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
    payload = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "gotv",
        "billersCode": "7032148522",
        "variation_code": "gotv-lite",
        "phone": "07046799872"
    }

    # Call the verify smartcard number method to make the payment request
    verify_smartCard_number = api.verify_smartCard_number(data)

    # Call the bouquet_change method to make the payment request
    change_bouquet = api.bouquet_change(payload)

    # Fetch service variations using the fetch_service_variations method
    network_name = "gotv"
    service_variations = api.fetch_service_variations(network_name)
    # print("Service Variations Response: ", service_variations)



