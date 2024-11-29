import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime as Mdate
import random, uuid


class VTPassAPI():
    def __init__(self, base_url, auth_token, secret_key):
        self.base_url = base_url
        self.auth_token = auth_token
        self.secret_key = secret_key
        self.headers = {
            "Authorization": self.auth_token,
            "Secret-Key": self.secret_key   
        }

    # BUY AIRTIME
    def buy_airtime(self, data):
        url = f"{self.base_url}/api/pay"
        print("POST URL: " + url)
        
        response = requests.post(url, json=data, auth=HTTPBasicAuth('oduwolesheriff001@gmail.com', 'Olamilekan1212'))
        print("Actual status code:", response.status_code)
        # print("Response content:", response.content)

        try:
            result = json.loads(response.text)
            json_str = json.dumps(result, indent=4)
            print("JSON POST response body: ", json_str)
            transaction_id = result["content"]["transactions"]["transactionId"]
            product_name = result["content"]["transactions"]["product_name"]
            print(f"Hellp Sheriff, you have successfully purchased {product_name} from vtpass, using transation id: {transaction_id}")
            return transaction_id
        except json.JSONDecodeError:
            print("Error decoding JSON response. Response content:")
            print(response.text)

        return None

if __name__ == "__main__":
    base_url = "https://sandbox.vtpass.com"
    auth_token = "Token be76014119dd44b12180ab93a92d63a2"
    secret_key = "SK_873dc5215f9063f6539ec2249c8268bb788b3150386"

    api = VTPassAPI(base_url, auth_token, secret_key)

    # Data For Post Request
    date_time_format = Mdate.now().strftime("%Y%m%d%H%M%S")

    def create_random_id():
        num = random.randint(1000, 4999)
        num_2 = random.randint(5000, 8000)
        num_3 = random.randint(111, 999) * 2
        return str(num) + str(num_2) + str(num_3) + str(uuid.uuid4())
    
    data = {
        'request_id': str(date_time_format) + create_random_id(),
        "serviceID": "MTN",
        'amount': 100,
        "phone": +23407046799872,
    }
    api.buy_airtime(data)