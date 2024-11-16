from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction as db_transaction

class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.username

    def deposit(self, amount: float):
        """ Method to deposit funds to the user balance """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        # Use an atomic transaction to ensure balance and transaction log are updated together
        with db_transaction.atomic():
            self.balance += amount
            self.save()  # Save the updated balance

            # Log the deposit transaction
            Transaction.objects.create(
                user=self,
                transaction_type='deposit',
                amount=amount
            )

    def withdraw(self, amount: float):
        """ Method to withdraw funds from the user balance """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        
        # Use an atomic transaction to ensure balance and transaction log are updated together
        with db_transaction.atomic():
            self.balance -= amount
            self.save()  # Save the updated balance

            # Log the withdrawal transaction
            Transaction.objects.create(
                user=self,
                transaction_type='withdrawal',
                amount=amount
            )

    def transfer(self, recipient, amount: float):
        """ Method to transfer funds from one user to another """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        
        # Use an atomic transaction to ensure balance and transaction log are updated together
        with db_transaction.atomic():
            # Deduct from sender and add to recipient
            self.balance -= amount
            recipient.balance += amount
            
            # Save both sender and recipient balance updates
            self.save()
            recipient.save()

            # Log the transaction for the sender
            Transaction.objects.create(
                user=self,
                transaction_type='transfer',
                amount=amount,
                recipient=recipient
            )

            # Log the transaction for the recipient
            Transaction.objects.create(
                user=recipient,
                transaction_type='transfer',
                amount=amount,
                recipient=self
            )
            

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # The user who initiated the transaction
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username} on {self.timestamp}"

