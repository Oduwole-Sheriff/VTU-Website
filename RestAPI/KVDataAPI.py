import requests
from django.conf import settings

class KVDataAPI:
    BASE_URL = "https://kvdataapi.net/api/data/"

    def __init__(self, token: str, use_bearer: bool = False):
        """
        Initialize KVDataAPI with your API token.
        :param token: Your API token string
        :param use_bearer: Some APIs require 'Bearer', others 'Token'
        """
        auth_prefix = "Bearer" if use_bearer else "Token"
        self.headers = {
            "Authorization": f"{auth_prefix} {token}",
            "Content-Type": "application/json"
        }

    def buy_data(self, network_id: int, mobile_number: str, plan_id: int, ported_number: bool = True):
        payload = {
            "network": network_id,          # must be int (pk)
            "mobile_number": mobile_number,
            "plan": plan_id,
            "Ported_number": ported_number  # 👈 capital P
        }

        try:
            response = requests.post(self.BASE_URL, headers=self.headers, json=payload)
            return {
                "status_code": response.status_code,
                "response": response.json()
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    TOKEN = settings.KVDATA_AUTH_TOKEN
    kv_api = KVDataAPI(TOKEN, use_bearer=False)

    result = kv_api.buy_data(
        network_id=1,                 
        mobile_number="09095263835",
        plan_id=442,            
        ported_number=True
    )
    print(result)
