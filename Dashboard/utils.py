from decimal import Decimal
from .models import CustomUser

def handle_first_deposit_reward(user: CustomUser, amount_paid: Decimal):
    if user.first_deposit_reward_given:
        return  # Already rewarded

    if user.balance >= Decimal('50.00'):
        user.balance -= Decimal('50.00')
        ten_percent = amount_paid * Decimal('0.03')

        if ten_percent <= Decimal('50.00'):
            bonus_share = Decimal('50.00') - ten_percent
            user.bonus += bonus_share
        else:
            # Deduct from balance instead
            extra_fee = ten_percent - Decimal('50.00')
            if user.balance >= extra_fee:
                user.balance -= extra_fee
            else:
                # You may want to log insufficient balance here
                print(f"User {user.username} has insufficient balance for extra Monnify fee.")

        if user.referred_by:
            # Give ₦10 to the referrer
            referrer = user.referred_by

            if user.bonus >= Decimal('10.00'):
                user.bonus -= Decimal('10.00')  # Take ₦10 from user's bonus
                referrer.referral_bonus += Decimal('10.00')
                # referrer.bonus += Decimal('10.00')  # Optional: also increase their general bonus
                referrer.save()

        user.first_deposit_reward_given = True
        user.save()


# def handle_first_deposit_reward(user: CustomUser):
#     if user.first_deposit_reward_given:
#         return  # Already rewarded, exit

#     if user.balance >= Decimal('50.00'):
#         # Deduct ₦50 from balance to bonus
#         user.balance -= Decimal('50.00')
#         user.bonus += Decimal('15.00')

#         if user.referred_by:
#             # Give ₦10 to the referrer
#             referrer = user.referred_by

#             if user.bonus >= Decimal('10.00'):
#                 user.bonus -= Decimal('10.00')  # Take ₦10 from user's bonus
#                 referrer.referral_bonus += Decimal('10.00')
#                 # referrer.bonus += Decimal('10.00')  # Optional: also increase their general bonus
#                 referrer.save()

#         user.first_deposit_reward_given = True
#         user.save()