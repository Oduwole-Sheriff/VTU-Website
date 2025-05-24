import os
import hmac

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import hashlib

from Dashboard.utils import handle_first_deposit_reward  
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from decimal import Decimal
import traceback
import json


from Dashboard.models import CustomUser, MonnifyTransaction

your_secret_key = os.environ["MONNIFY_CLIENT_SECRET"]  # Your Monnify Secret key
monnify_ip = os.environ["MONNIFY_IP"]  # Monnify IP address which is: 35.242.133.146


def verify_hash(payload_in_bytes, monnify_hash):
    secret_key_bytes = os.environ["MONNIFY_CLIENT_SECRET"].encode("utf-8")
    your_hash_in_bytes = hmac.new(
        secret_key_bytes, msg=payload_in_bytes, digestmod=hashlib.sha512
    )
    your_hash_in_hex = your_hash_in_bytes.hexdigest()
    return hmac.compare_digest(your_hash_in_hex, monnify_hash)



def get_sender_ip(headers):
    """
    Get senders' IP address, by first checking if your API server
    is behind a proxy by checking for HTTP_X_FORWARDED_FOR
    if not gets sender actual IP address using REMOTE_ADDR
    """

    x_forwarded_for = headers.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # in some cases this might be in the second index ie [1]
        # depending on your hosting environment
        return x_forwarded_for.split(",")[0]
    else:
        return headers.get("REMOTE_ADDR")


def verify_monnify_webhook(payload_in_bytes, monnify_hash, headers):
    """
    The interface that does the verification by calling necessary functions.
    Though everything has been tested to work well, but if you have issues
    with this function returning False, you can remove the get_sender_ip
    function to be sure that the verify_hash is working, then you can check
    what header contains the IP address.
    """

    return get_sender_ip(headers) == monnify_ip and verify_hash(
        payload_in_bytes, monnify_hash
    )

@api_view(["POST"])
def process_webhook(request):
    """
    A function based view implementing the receipt of the webhook payload.
    The webhook payload should be received as bytes rather than json
    that would be converted to bytes.This is most likely one of the
    cause for failed webhook verification.
    After the webhook verification, you can get a json format of the byte
    object by simply calling json.loads(payload_in_bytes)
    """

    payload_in_bytes = request.body
    monnify_hash = request.META["HTTP_MONNIFY_SIGNATURE"]
    confirmation = verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META)
    if confirmation is False:
        return Response(
            {"status": "failed", "msg": "Webhook does not appear to come from Monnify"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        """
        if payload verification is successful, you can perform your necessary task,
        but if your planned processing would take time, you should first return a 200 response
        and process your stuff in background.
        """
        return Response(
            {"status": "success", "msg": "Webhook received successfully"},
            status=status.HTTP_200_OK,
        )

class WebhookView(APIView):
    def post(self, request):
        payload_in_bytes = request.body
        monnify_hash = request.META.get("HTTP_MONNIFY_SIGNATURE")

        if not monnify_hash:
            return Response(
                {"status": "failed", "message": "Missing Monnify signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_monnify_webhook(payload_in_bytes, monnify_hash, request.META):
            return Response(
                {"status": "failed", "message": "Invalid Monnify signature or IP"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = json.loads(payload_in_bytes.decode("utf-8"))
            event_type = payload.get("eventType")

            if event_type != "SUCCESSFUL_TRANSACTION":
                return Response(
                    {"status": "success", "message": "Event not processed"},
                    status=status.HTTP_200_OK
                )

            event_data = payload.get("eventData", {})
            payment_reference = event_data.get("paymentReference")
            amount_paid = Decimal(str(event_data.get("amountPaid", "0")))
            customer_email = event_data.get("customer", {}).get("email")
            account_reference = event_data.get("product", {}).get("reference")

            # Get user
            user = None
            if customer_email:
                try:
                    user = CustomUser.objects.get(email__iexact=customer_email)
                except CustomUser.DoesNotExist:
                    pass
            if not user and account_reference:
                username_part = account_reference.split('_')[-1]
                try:
                    user = CustomUser.objects.get(username__iexact=username_part)
                except CustomUser.DoesNotExist:
                    pass

            if not user:
                return Response(
                    {"status": "success", "message": "User not found"},
                    status=status.HTTP_200_OK,
                )

            if MonnifyTransaction.objects.filter(payment_reference=payment_reference).exists():
                return Response(
                    {"status": "success", "message": "Duplicate webhook"},
                    status=status.HTTP_200_OK,
                )

            # Credit user
            user.balance = (user.balance or Decimal('0.00')) + amount_paid
            user.save()

            # Check and apply first deposit reward
            was_first_deposit = not getattr(user, 'first_deposit_reward_given', True)
            handle_first_deposit_reward(user)

            # Deduct Monnify transaction fee
            monnify_fee = Decimal(getattr(settings, "MONNIFY_TRANSACTION_FEE", "35.00"))
            should_deduct_fee = getattr(user, 'first_deposit_reward_given', False)

            if should_deduct_fee and user.balance >= monnify_fee:
                user.balance -= monnify_fee
                user.save()

            # Log transaction
            MonnifyTransaction.objects.create(
                user=user,
                amount=amount_paid,
                payment_reference=payment_reference,
                monnify_transaction_reference=event_data.get("transactionReference"),
                bank_code=event_data.get("paymentSourceInformation", [{}])[0].get("bankCode", ""),
                account_number=event_data.get("paymentSourceInformation", [{}])[0].get("accountNumber", ""),
                narration=event_data.get("narration", "User Deposit"),
                status='successful',
                currency=event_data.get("currencyCode", "NGN"),
                response_message=payload,
                transaction_type='first_deposit' if was_first_deposit else 'regular_deposit',
                date=now()
            )

            # Send email
            try:
                send_mail(
                    subject="Wallet Credited Successfully",
                    message=f"Hello {user.username},\n\nYour wallet has been credited with {amount_paid:,.2f}.\nNew balance: {user.balance:,.2f}.\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as mail_err:
                print(f"🔥 Error sending confirmation email: {mail_err}")

            return Response(
                {"status": "success", "message": "Wallet credited successfully"},
                status=status.HTTP_200_OK
            )

        except json.JSONDecodeError as e:
            return Response({"status": "failed", "message": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"🔥 Internal error: {str(e)}")
            print(traceback.format_exc())
            return Response({"status": "error", "message": "Internal processing error"}, status=status.HTTP_200_OK)
