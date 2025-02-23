import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime as Mdate
import random
import uuid

# VTPassDataAPI class definition
class VTPassElectricity:
    def __init__(self, base_url, auth_token, secret_key):
        self.base_url = base_url
        self.auth_token = auth_token
        self.secret_key = secret_key
        self.headers = {
            "Authorization": self.auth_token,
            "Secret-Key": self.secret_key   
        }

    def verify_meter_number(self, data):
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

    def Meter_payment(self, payload):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
        # Sending POST request to the API
        response = requests.post(url, json=payload, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)

        try:
            result = response.json()  # Directly parse the JSON response
            print("JSON PREPAID response body: ", json.dumps(result, indent=4))
            return result  # Return the full response (not just transaction ID)
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)
            return None

    def Postpaid_meter_payment(self, postpay):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
        # Sending POST request to the API
        response = requests.post(url, json=postpay, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)

        try:
            result = response.json()  # Directly parse the JSON response
            print("JSON POSTPAID response body: ", json.dumps(result, indent=4))
            return result  # Return the full response (not just transaction ID)
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)
            return None

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
    api = VTPassElectricity(base_url, auth_token, secret_key)

    data = {
        "billersCode": 1010101010101,
        "serviceID": "ikeja-electric",
        'type': "postpaid"
    }

    # Data for POST request
    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
    payload = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "ikeja-electric",
        "billersCode": "1111111111111",
        "variation_code": "prepaid",
        'amount': 1000,
        "phone": "07046799872"
    }

    # Data for POST request
    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")
    postpay = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "eko-electric",
        "billersCode": "1010101010101",
        "variation_code": "postpaid",
        'amount': 1000,
        "phone": "07046799872"
    }

    # Call the verify smartcard number method to make the payment request
    verify_meter_number = api.verify_meter_number(data)

    # Call the Meter_payment method to make the payment request
    Meter_payment = api.Meter_payment(payload)

     # Call the Meter_payment method to make the payment request
    Postpaid_meter_payment = api.Postpaid_meter_payment(postpay)




