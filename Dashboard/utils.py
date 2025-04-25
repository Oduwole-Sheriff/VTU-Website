from decimal import Decimal
from .models import CustomUser

def handle_first_deposit_reward(user: CustomUser):
    if user.first_deposit_reward_given:
        return  # Already rewarded, exit

    if user.balance >= Decimal('50.00'):
        # Deduct ₦50 from balance to bonus
        user.balance -= Decimal('50.00')
        user.bonus += Decimal('15.00')

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
