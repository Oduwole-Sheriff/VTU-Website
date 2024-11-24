from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction as db_transaction


class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bank_account = models.JSONField(blank=True, null=True)  # Bank account details as JSONField
    nin = models.CharField(max_length=20, blank=True, null=True)
    bvn = models.CharField(max_length=11, blank=True, null=True, unique=True)  # BVN field added

    def __str__(self):
        return self.username


    def deposit(self, amount: float):
        """ Method to deposit funds to the user balance """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
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
        
        with db_transaction.atomic():
            self.balance -= amount
            recipient.balance += amount
            
            self.save()
            recipient.save()

            # Log the transaction for the sender
            Transaction.objects.create(
                user=self,
                transaction_type='transfer',
                amount=amount,
                recipient=recipient  # Ensure correct reference to recipient's user
            )

            # Log the transaction for the recipient
            Transaction.objects.create(
                user=recipient,
                transaction_type='transfer',
                amount=amount,
                recipient=self  # Correct reference to sender's user
            )


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username} on {self.timestamp}"


class WebsiteConfiguration(models.Model):
    base_url = models.URLField(max_length=255)
    auth_token = models.CharField(max_length=500)

    def __str__(self):
        return f"Monnify API Configuration"

    @classmethod
    def get_configuration(cls):
        """
        Method to retrieve the current Monnify API configuration
        """
        config = cls.objects.first()
        if config:
            return config.base_url, config.auth_token
        return None, None

    @classmethod
    def update_configuration(cls, base_url, auth_token):
        """
        Method to update the Monnify API configuration in the database
        """
        config, created = cls.objects.get_or_create(id=1)  # Assuming only one configuration entry
        config.base_url = base_url
        config.auth_token = auth_token