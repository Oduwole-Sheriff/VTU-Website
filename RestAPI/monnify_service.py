# import requests
# from django.conf import settings
# from Dashboard.models import CustomUser
# import logging


import base64
import json

# Your input string
input_string = "MK_TEST_36CS1B1AD6:R29WUNU3GGP276CXDVJYUPW0JZKUTEQ8"

# Convert string to bytes
input_bytes = input_string.encode('utf-8')

# Encode the bytes to Base64
base64_bytes = base64.b64encode(input_bytes)

# Convert Base64 bytes back to string for display
base64_string = base64_bytes.decode('utf-8')

print("Base64 Encoded:", base64_string)


# class MonnifyAPI:
#     def __init__(self, base_url=None, auth_token=None):
#         self.base_url = base_url or settings.MONNIFY_BASE_URL
#         self.auth_token = auth_token or settings.MONNIFY_AUTH_TOKEN

#     def create_account(self, data):
#         """ Call the Monnify API to create a reserved account for the user """
#         headers = {
#             'Authorization': f'Bearer {self.auth_token}',
#             'Content-Type': 'application/json',
#         }

#         response = requests.post(
#             f'{self.base_url}/api/v2/bank-transfer/reserved-accounts',
#             headers=headers,
#             json=data
#         )

#         if response.status_code == 200:
#             return response.json()  # Assuming the response is in JSON format
#         else:
#             return {"requestSuccessful": False, "responseMessage": "Error in creating account."}


# logger = logging.getLogger(__name__)

# def create_monnify_account_for_user(user: CustomUser):
#     """Create a Monnify reserved account for the user and save the response to the user model."""
    
#     # Initialize the Monnify API client
#     api = MonnifyAPI(base_url=settings.MONNIFY_BASE_URL, auth_token=settings.MONNIFY_AUTH_TOKEN)

#     # Prepare the request data
#     data = {
#         "accountReference": str(user.id),  # Use the user ID as the account reference
#         "accountName": user.username,
#         "currencyCode": "NGN",
#         "contractCode": "5347308431",  # Replace with your Monnify contract code
#         "customerEmail": user.email,
#         "customerName": user.username,
#         "nin": user.nin,  # Assuming NIN is set on the user
#         "getAllAvailableBanks": True
#     }

#     try:
#         # Send request to create the account
#         response = api.create_account(data)

#         # Log the response for debugging purposes
#         logger.info(f"Monnify account creation response: {response}")

#     except Exception as e:
#         # Handle any exception during the API request
#         logger.error(f"Error while creating Monnify account: {str(e)}")
#         return {"requestSuccessful": False, "responseMessage": "An error occurred while processing your request."}

#     # Check if the response indicates success
#     if response.get("requestSuccessful"):
#         # Extract the response body
#         response_body = response.get("responseBody", {})

#         # Log the response body (useful for debugging)
#         logger.info(f"Monnify response body: {response_body}")

#         # Save the response body in the user's bank_account field
#         user.bank_account = response_body  # This will save the entire response body as JSON
#         user.save()

#         # Log the successful save
#         logger.info(f"Monnify account details saved for user {user.username}")

#         return {"requestSuccessful": True, "responseMessage": "Monnify account created successfully."}
#     else:
#         # Return failure if Monnify account creation fails
#         return {"requestSuccessful": False, "responseMessage": "Failed to create Monnify account. Please try again."}