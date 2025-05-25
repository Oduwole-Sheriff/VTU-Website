import requests
import json
from requests.auth import HTTPBasicAuth
import uuid
from django.conf import settings
import os

class MonnifyBankTransferAPI:
    def __init__(self, base_url, auth_token, secret_key):
        self.base_url = base_url
        self.auth_token = auth_token
        self.secret_key = secret_key
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Secret-Key": self.secret_key
        }

    def get_access_token(self):
        """Get access token using API keys"""
        url = f"{self.base_url}/api/v1/auth/login"
        credentials = HTTPBasicAuth(self.auth_token, self.secret_key)

        response = requests.post(url, auth=credentials)
        if response.status_code == 200:
            token = response.json()['responseBody']['accessToken']
            return token
        else:
            print("Auth failed:", response.text)
            return None

    def send_bonus_to_platform(self, amount, bank_code, account_number, reference=None):
        """Send bonus to user via bank transfer"""
        if not reference:
            reference = str(uuid.uuid4())  # Generate unique reference

        url = f"{self.base_url}/api/v2/disbursements/single"
        print("Starting disbursement...")

        token = self.get_access_token()
        if not token:
            print("Could not get token")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "amount": amount,
            "reference": reference,
            "narration": "User Bonus Withdrawal",
            "destinationBankCode": bank_code,
            "destinationAccountNumber": account_number,
            "sourceAccountNumber": "8065931760",  # Your source account number
            "walletId": "default",  # Default wallet
            "currency": "NGN"
        }

        print("Payload:", json.dumps(payload, indent=4))

        response = requests.post(url, headers=headers, json=payload)
        print("Status code:", response.status_code)

        try:
            json_data = response.json()
            print("Disbursement response:", json.dumps(json_data, indent=4))
            return json_data
        except json.JSONDecodeError:
            print("Error decoding disbursement response:", response.text)
            return None
        
    def create_sub_account(self, payload2):
        url = f"{self.base_url}/api/v1/sub-accounts"
        print("Creating SubAccount Loading...")

        token = self.get_access_token()
        if not token:
            print("Could not get token")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Log the payload before sending the request
        print("Payload:", json.dumps(payload2, indent=4))

        # Make the POST request to create sub-account
        response = requests.post(url, headers=headers, json=payload2)
        print("Status code:", response.status_code)

        try:
            json_data = response.json()
            print("SubAccount response:", json.dumps(json_data, indent=4))
            return json_data
        except json.JSONDecodeError:
            print("Error decoding SubAccount response:", response.text)
            print("Raw Response Text:", response.text)  # For more details
            return None

    def get_sub_accounts(self):
        """Fetch all sub-accounts created under the Monnify integration"""
        url = f"{self.base_url}/api/v1/sub-accounts"
        
        print("Fetching sub-accounts...")

        # Fetch a new token if the previous one is expired
        token = self.get_access_token()
        if not token:
            print("Failed to obtain token. Exiting.")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print("Sub Accounts response:", json.dumps(json_data, indent=4))
                return json_data
            except json.JSONDecodeError:
                print("Error decoding response:", response.text)
                return None
        else:
            print(f"Failed to fetch sub-accounts. Status Code: {response.status_code}")
            print("Response:", response.text)
            return None



# Entry point for script testing
if __name__ == "__main__":
    base_url = "https://api.monnify.com"
    auth_token = "MK_PROD_FZBUQ7AH61"  # Your Monnify test API key
    secret_key = "NM3B82KQT2F31F3RE0J0RKLQ8AECJ6VZ"  # Your Monnify test secret key

    api = MonnifyBankTransferAPI(base_url, auth_token, secret_key)

    # Example: Send Bonus
    api.send_bonus_to_platform(
        amount=5000,
        bank_code="058",  # GTBank
        account_number="0123456789",
        reference=f"bonus-withdrawal-test-001-{uuid.uuid4()}"
    )

    payload2 = [
        {
            "currencyCode": "NGN",  # Currency code (NGN)
            "bankCode": "057",      # Bank code (verify if this is correct for the selected bank)
            "accountNumber": "2417372510",  # Your account number
            "email": "bigsheriffdevelopers089@gmail.com",  # Email tied to the sub account
            "defaultSplitPercentage": 20.87  # Split percentage
        }
    ]

    # Call the function to create sub-account
    create_sub_account = api.create_sub_account(payload2)

    # Get sub-accounts and print the response
    api.get_sub_accounts()