import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime as Mdate
import random
import uuid

# VTPassEducationAPI class definition
class VTPassEducationAPI:
    def __init__(self, base_url, auth_token, secret_key):
        self.base_url = base_url
        self.auth_token = auth_token
        self.secret_key = secret_key
        self.headers = {
            "Authorization": self.auth_token,
            "Secret-Key": self.secret_key
        }

    # BUY DATA method
    def Waec_Registration_pin(self, data):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
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
        
    def Verify_jamb_profile(self, datacom):
        url = f"{self.base_url}/api/merchant-verify"
        print("POST URL: " + url)
        
        # Sending POST request to the API
        response = requests.post(url, json=datacom, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)

        try:
            result = response.json()  # Directly parse the JSON response
            print("JSON POST response body: ", json.dumps(result, indent=4))
            return result  # Return the full response (not just transaction ID)
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)
            return None

    def Jamb_Vending_Pin(self, datacom2):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
        # Sending POST request to the API
        response = requests.post(url, json=datacom2, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
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
        url = "https://sandbox.vtpass.com/api/service-variations?serviceID=waec-registration"
        payload = json.dumps({
            "serviceID": f"{network_name}"
        })
        headers = {
            'Authorization': '',
            'Content-Type': 'application/json',
            'Cookie': 'bootstrap_coli_ce=eyJpdiI6ImlGWE1HUjRMeVhPTDI0cFZ1ZXVaSHc9PSIsInZhbHVlIjoieEtsbCsyVkhHS3hMNGVJb1JNUklWc2FOYVwvdWtBZDlJM2xJY3NDTm5LdEJHb0hRaEZtNXdpbTZBXC9oVTRWQjlxIiwibWFjIjoiNjY2YTRjYjE5MzZiZjY1ZGM4YjUyMWI2Y2FjM2U3YjEzYWViOTdjYmVkM2MzMGU2ZDUxYzEzY2MwNTc4NDYyYiJ9; laravel_session=eyJpdiI6IjFJcXRPZlBqcUR6SEREcE5sTnZQVFE9PSIsInZhbHVlIjoiOERMXC96azRwb3l2UUE4R1hMMkVyYllEZVZJNHJzZmN1NmtCaGd5ZVZKWTRkeWpHTWZQZ29tYWtQYWZWMXRPcEdcL1A3R0owMlYweFdHMGJkck9IN1wvMWc9PSIsIm1hYyI6IjdmZDM1M2ZhNzg0MGNlNThhNTkyZTEwZDcwMzI5ODZlMjAyZmVhODI5Yjk1Yjc5MDQ5OTkwNDQxODFlMTliZWYifQ%3D%3D'
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

    # Instantiate VTPassEducationAPI object
    api = VTPassEducationAPI(base_url, auth_token, secret_key)

    # Data for POST request
    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
    data = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "waec-registration",
        "variation_code": "waec-registraion",
        "quantity": "1",
        "phone": "07046799872"
    }

    datacom = {
        'billersCode': "0123456789",
        "serviceID": "jamb",
        "type": "utme-mock",
    }

    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
    datacom2 = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "jamb",
        "variation_code": "utme-no-mock",
        "billersCode": "0123456789",
        "phone": "07046799872"
    }

    # Call the Waec_Registration_pin method to make the payment request
    waec_registration_pin = api.Waec_Registration_pin(data)

    verify_jamb_profile = api.Verify_jamb_profile(datacom)

    jamb_vending_pin = api.Jamb_Vending_Pin(datacom2)

    # Fetch service variations using the fetch_service_variations method
    network_name = "waec-registration"
    service_variations = api.fetch_service_variations(network_name)
    # print("Service Variations Response: ", service_variations)
