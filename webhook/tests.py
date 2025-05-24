# import os
# import hmac
# import hashlib
# import json

# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.urls import reverse

# from webhook.views import verify_hash  # Ensure this points to your actual views.py


# class EnvironmentTest(TestCase):
#     def test_that_monnify_secret_is_set(self):
#         self.assertIsNot(os.getenv("MONNIFY_CLIENT_SECRET", None), None)

#     def test_that_monnify_ip_is_set(self):
#         self.assertIsNot(os.getenv("MONNIFY_IP", None), None)


# class UtilsTest(TestCase):
#     def setUp(self):
#         os.environ["MONNIFY_CLIENT_SECRET"] = "Monnify"

#     def test_hashing_function(self):
#         payload_in_bytes = b'test-payload'
#         secret_key = os.environ.get("MONNIFY_CLIENT_SECRET", "dummy_secret")

#         expected_hash = hmac.new(
#             secret_key.encode("utf-8"),
#             msg=payload_in_bytes,
#             digestmod=hashlib.sha512
#         ).hexdigest()

#         self.assertTrue(verify_hash(payload_in_bytes, expected_hash))

#     def test_ip_checker(self):
#         os.environ["MONNIFY_IP"] = "35.242.133.146"
#         self.assertEqual(os.getenv("MONNIFY_IP"), "35.242.133.146")


# class ViewTest(TestCase):
#     def setUp(self):
#         # Ensure environment variables are set before any imports or execution
#         os.environ["MONNIFY_CLIENT_SECRET"] = "Monnify"
#         os.environ["MONNIFY_IP"] = "35.242.133.146"

#         self.secret_key = os.environ["MONNIFY_CLIENT_SECRET"]
#         self.valid_ip = os.environ["MONNIFY_IP"]

#         self.payload = b'''{
#             "eventType": "SUCCESSFUL_TRANSACTION",
#             "eventData": {
#                 "amountPaid": "1000",
#                 "paymentReference": "abc123",
#                 "customer": {"email": "test@example.com"},
#                 "product": {"reference": "user_test"},
#                 "paymentSourceInformation": [{"bankCode": "001", "accountNumber": "1234567890"}],
#                 "transactionReference": "txn_001",
#                 "narration": "Funding",
#                 "currencyCode": "NGN"
#             }
#         }'''

#         self.signature = hmac.new(
#             self.secret_key.encode("utf-8"),
#             msg=self.payload,
#             digestmod=hashlib.sha512
#         ).hexdigest()

#     def test_class_based_view(self):
#         url = reverse("monnify-webhook")
#         client = APIClient()
#         response = client.post(
#             url,
#             data=self.payload,
#             content_type="application/json",
#             HTTP_MONNIFY_SIGNATURE=self.signature,
#             REMOTE_ADDR=self.valid_ip
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_func_based_view(self):
#         url = reverse("process_webhook")
#         client = APIClient()
#         response = client.post(
#             url,
#             data=self.payload,
#             content_type="application/json",
#             HTTP_MONNIFY_SIGNATURE=self.signature,
#             REMOTE_ADDR=self.valid_ip
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_class_view_invalid_signature(self):
#         url = reverse("monnify-webhook")
#         client = APIClient()
#         invalid_signature = "invalidsignature123456"

#         response = client.post(
#             url,
#             data=self.payload,
#             content_type="application/json",
#             HTTP_MONNIFY_SIGNATURE=invalid_signature,
#             REMOTE_ADDR=self.valid_ip
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['message'], "Invalid Monnify signature or IP")

#     def test_class_view_invalid_ip(self):
#         url = reverse("monnify-webhook")
#         client = APIClient()

#         response = client.post(
#             url,
#             data=self.payload,
#             content_type="application/json",
#             HTTP_MONNIFY_SIGNATURE=self.signature,
#             REMOTE_ADDR="192.168.0.1"  # Wrong IP
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['message'], "Invalid Monnify signature or IP")

#     def test_class_view_missing_signature(self):
#         url = reverse("monnify-webhook")
#         client = APIClient()

#         response = client.post(
#             url,
#             data=self.payload,
#             content_type="application/json",
#             REMOTE_ADDR=self.valid_ip
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json()['message'], "Missing Monnify signature")



