import requests
import base64
import json
from Dashboard.models import WebsiteConfiguration

# Your input string
input_string = "MK_TEST_T7B7RH8KVV:EVNSMUKE3YB0WMX4BL959DFBC2H1P11E"

# Convert string to bytes
input_bytes = input_string.encode('utf-8')

# Encode the bytes to Base64
base64_bytes = base64.b64encode(input_bytes)

# Convert Base64 bytes back to string for display
base64_string = base64_bytes.decode('utf-8')

print("Base64 Encoded:", base64_string)


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


# class MonnifyAPI():
#     def __init__(self, base_url, auth_token):
#         self.base_url = base_url
#         self.auth_token = auth_token
#         self.headers = {"Authorization": self.auth_token}
    
#     # New method to handle login
#     def login(self):
#         url = f"{self.base_url}/api/v1/auth/login"
#         headers = {
#             'Authorization': 'Basic TUtfVEVTVF9XTjlZRDNEVFJHOjFWWlNZTEY3UThaM1haUkxXQzhBVTlHS0VaNEQ5WDNZ',
#             'Cookie': 'JSESSIONID=9825E24E0CC14F3CDA4BACE97F546908'
#         }

#         # No data is required as per the curl command
#         response = requests.post(url, headers=headers)
#         print("Login POST URL: " + url)
        
#         print("Actual status code:", response.status_code)
#         print("Response content:", response.content)

#         try:
#             json_data = response.json()
#             json_str = json.dumps(json_data, indent=4)
#             print("JSON Login response body: ", json_str)
#             if response.status_code == 200:
#                 print("Login successful.")
#             else:
#                 print("Login failed.")
#             return json_data
#         except json.JSONDecodeError:
#             print("Error decoding JSON response. Response content:")
#             print(response.text)

#         return None

#     def get_account_details(self, data):
#         url = f"{self.base_url}/api/v2/bank-transfer/reserved-accounts"
#         print("POST URL: " + url)
        
#         response = requests.post(url, json=data, headers=self.headers)
#         print("Actual status code:", response.status_code)
#         print("Response content:", response.content)

#         try:
#             json_data = response.json()
#             json_str = json.dumps(json_data, indent=4)
#             print("JSON POST response body: ", json_str)
#             user_id = json_data.get("id")
#             print("User ID ===>", user_id)
#             print(".......POST/DATA TopUp Is Done.......")
#             print(".......=====================.......")
#             return user_id
#         except json.JSONDecodeError:
#             print("Error decoding JSON response. Response content:")
#             print(response.text)

#         return None

# if __name__ == "__main__":
#     base_url = "https://sandbox.monnify.com"
#     auth_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsibW9ubmlmeS12YWx1ZS1hZGRlZC1zZXJ2aWNlIiwibW9ubmlmeS1wYXltZW50LWVuZ2luZSIsIm1vbm5pZnktZGlzYnVyc2VtZW50LXNlcnZpY2UiLCJtb25uaWZ5LW9mZmxpbmUtcGF5bWVudC1zZXJ2aWNlIl0sInNjb3BlIjpbInByb2ZpbGUiXSwiZXhwIjoxNzMxOTY5NTc3LCJhdXRob3JpdGllcyI6WyJNUEVfTUFOQUdFX0xJTUlUX1BST0ZJTEUiLCJNUEVfVVBEQVRFX1JFU0VSVkVEX0FDQ09VTlQiLCJNUEVfSU5JVElBTElaRV9QQVlNRU5UIiwiTVBFX1JFU0VSVkVfQUNDT1VOVCIsIk1QRV9DQU5fUkVUUklFVkVfVFJBTlNBQ1RJT04iLCJNUEVfUkVUUklFVkVfUkVTRVJWRURfQUNDT1VOVCIsIk1QRV9ERUxFVEVfUkVTRVJWRURfQUNDT1VOVCIsIk1QRV9SRVRSSUVWRV9SRVNFUlZFRF9BQ0NPVU5UX1RSQU5TQUNUSU9OUyJdLCJqdGkiOiJlMDMyMjVlMC0zYjU5LTQxOTgtOWIxNC04MTEwOGI5YWViNDQiLCJjbGllbnRfaWQiOiJNS19URVNUX1dOOVlEM0RUUkcifQ.jvnEwfy299u0SZ_hAAwnFNfGxh9-3GGwwEGoGJMc4vKdpaAekKkQc-Ws52xnc5RkSy8jLL7VbNEuqNMW7fPXsdqPk0Uw7_kyM1LR6F6K62QFbsUfbMz8Gp4CMYVciVdpGj9IhtejPs4ogOaXKxvS5MGekeHDLcE6KTlgT8zmVDDiuNmjLdVldVJjSgXdt0I6uOU8xzhkcUovCfog80I7YFtDKT4er5u3qMx49SERwVtTSKqYFgGW-E1xBjOuw8UYvbreWX3i27EzDCspDHijD9iFlGU_P36tyR8HhZkz_tL1XlV83gIRfJAL_DthBsKEU2J-5W73QgNmU7ydIu4oQA"

#     api = MonnifyAPI(base_url, auth_token)

#     # First, login to get authorization (if necessary)
#     login_data = api.login()

#     # DATA FOR POST REQUEST (Assuming login is successful)
#     if login_data:
#         data = { 
#             "accountReference": "abc123d4730",
#             "accountName": "ysbbs hsbsb nxnyhyehznq",
#             "currencyCode": "NGN",
#             "contractCode": "5347308431",
#             "customerEmail": "jxbbzww@qq.com",
#             "customerName": "ysbbs hsbkfkjsb nxnznq",
#             "nin":"34848098058",
#             "getAllAvailableBanks": True
#         }
#         api.get_account_details(data)
