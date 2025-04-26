import requests
import json
from requests.auth import HTTPBasicAuth
import uuid
from django.conf import settings

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
            "sourceAccountNumber": "4877178978",  # Your source account number
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

    def send_to_reserved_account(self, amount, reservation_reference, reference=None):
        """Send funds to a reserved account"""
        if not reference:
            reference = str(uuid.uuid4())  # Generate unique reference

        url = f"{self.base_url}/api/v2/disbursements/single"  # Adjusted to simulate transaction
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
            "reference": reference,  # Unique reference for the transaction
            "narration": "Testing Reserved Account Credit",  # Description of the payment
            "destinationBankCode": "232",  # Bank code, for example, GTBank is '057'
            "destinationAccountNumber": "2245781956",  # Example account number
            "currency": "NGN",  # Currency
            "sourceAccountNumber": "4877178978",  # Your source account number (ensure it's valid)
            "contractCode": "5347308431",  # Example contract code
            "paymentMethods": ["ACCOUNT_TRANSFER"],  # Payment method (this could be other methods as well)
            "reservationReference": reservation_reference  # Reserved account reference
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


# Entry point for script testing
if __name__ == "__main__":
    base_url = "https://sandbox.monnify.com"
    auth_token = settings.MONNIFY_CLIENT_ID  # Your Monnify test API key
    secret_key = settings.MONNIFY_CLIENT_SECRET  # Your Monnify test secret key

    api = MonnifyBankTransferAPI(base_url, auth_token, secret_key)

    # Example: Send Bonus
    api.send_bonus_to_platform(
        amount=5000,
        bank_code="058",  # GTBank
        account_number="0123456789",
        reference=f"bonus-withdrawal-test-001-{uuid.uuid4()}"
    )

    response = api.send_to_reserved_account(
        amount=1000,
        reservation_reference="73BA6JCHCVQ7AJQ00504122",  # Example reservation reference
        reference=f"payment-to-reserved-account-{uuid.uuid4()}"
    )
