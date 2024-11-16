from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from .models import CustomUser, Transaction

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

