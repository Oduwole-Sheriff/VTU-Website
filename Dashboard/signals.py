from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from .models import CustomUser, Transaction
from RestAPI.monnifyAPI import MonnifyAPI
import requests
import base64
import uuid
import datetime

@receiver(post_save, sender=CustomUser)
def create_transaction_log(sender, instance, created, **kwargs):
    """
    This signal will create a transaction log whenever the balance of a user is updated.
    We use the post_save signal to track changes to balance after save.
    """
    if not created:
        # Check if the balance has changed, indicating a deposit or withdrawal
        if hasattr(instance, '_prev_balance') and instance.balance != instance._prev_balance:
            if instance.balance > instance._prev_balance:
                transaction_type = 'deposit'
                amount = instance.balance - instance._prev_balance
            elif instance.balance < instance._prev_balance:
                transaction_type = 'withdrawal'
                amount = instance._prev_balance - instance.balance
            else:
                return  # No change, do nothing
                
            # Create transaction log
            Transaction.objects.create(
                user=instance,
                transaction_type=transaction_type,
                amount=amount
            )
            
        elif hasattr(instance, '_prev_balance') and instance.balance == instance._prev_balance:
            return  # No balance change, do nothing.
        

def log_transfer(sender, instance, created, **kwargs):
    if created and instance.transaction_type == 'transfer':
        if instance.recipient is None:
            raise ValueError("Recipient is missing for transfer.")
        if not instance.recipient.pk:
            raise ValueError("Invalid recipient user.")
        if not instance.user.pk:
            raise ValueError("Invalid sender user.")

        # Save the transaction
        Transaction.objects.create(
            user=instance.user,
            transaction_type=instance.transaction_type,
            amount=instance.amount,
            recipient=instance.recipient
        )


@receiver(post_save, sender=CustomUser)
def create_account_details_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Step 1: Prepare the Basic Authorization Header
        client_id = "MK_TEST_XZMGHMDDFF"  # Replace with your Monnify client ID
        client_secret = "WEDYDDCGYEX98Z7L31R1RZ4V6LK12JK9"  # Replace with your Monnify client secret

        # Create a Basic Auth string in the format client_id:client_secret
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        # Step 2: Make the POST request to get the access token with the Authorization header
        auth_url = "https://sandbox.monnify.com/api/v1/auth/login"  # Authentication endpoint

        headers = {
            'Authorization': f'Basic {encoded_credentials}',  # Basic authentication header
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Send a POST request to get the access token
        auth_response = requests.post(auth_url, headers=headers)

        # Check if authentication was successful
        if auth_response.status_code == 200:
            auth_token = auth_response.json().get("responseBody", {}).get("accessToken")
            if not auth_token:
                print("Error: Access token not found in the response.")
                return

            # Debugging: Print the token to verify it's correctly retrieved
            print(f"Access Token: {auth_token}")

            # Step 3: Initialize the MonnifyAPI with the obtained Bearer token
            api = MonnifyAPI(
                base_url="https://sandbox.monnify.com",
                auth_token=f"Bearer {auth_token}"  # Set the Bearer token dynamically
            )

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = uuid.uuid4().hex[:6]  # 6-char unique suffix

            # Step 4: Prepare the data for account details request
            data = {
                "accountReference": f"user_{instance.id}_{instance.username}_{timestamp}_{unique_id}",  # Unique account reference
                "accountName": instance.username,  # Use the user's name
                "currencyCode": "NGN",
                "contractCode": "5347308431",
                "customerEmail": instance.email,  # Use the user's email
                "customerName": instance.username,  # Use the user's name
                "bvn": instance.bvn, # Use the user's BVN
                "nin": instance.nin,  # Use the user's NIN
                "getAllAvailableBanks": True
            }

            # Step 5: Make the API call to get account details
            reserved_accounts_url = "https://sandbox.monnify.com/api/v2/bank-transfer/reserved-accounts"
            headers = {
                'Authorization': f'Bearer {auth_token}',  # Bearer token added here
                'Content-Type': 'application/json'  # Set Content-Type to application/json
            }

            # Ensure data is correctly sent as JSON
            post_response = requests.post(reserved_accounts_url, json=data, headers=headers)

            # Debugging: Print the response
            print(f"Post Response Status Code: {post_response.status_code}")
            print(f"Post Response: {post_response.text}")

            # Step 6: If successful, save the response body in the bank_account field
            if post_response.status_code == 200:
                response_data = post_response.json()

                # Check if the Monnify response is successful
                if response_data.get("requestSuccessful"):
                    # Extract the response body
                    response_body = response_data.get("responseBody", {})

                    # Save the response body in the user's bank_account field
                    instance.bank_account = response_body  # Save the full response body as JSON
                    instance.save()

                    print("Monnify account details saved successfully.")

                else:
                    print(f"Error creating Monnify account: {response_data.get('responseMessage')}")
            else:
                print(f"Failed to create Monnify account. Status code: {post_response.status_code}")

        else:
            # Log or handle the error if token retrieval fails
            print("Error: Unable to fetch access token.")
            print(f"Auth Response Code: {auth_response.status_code}")
            print(f"Auth Response: {auth_response.text}")  # Print the full error message for debugging
