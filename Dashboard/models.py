from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import F
from django.db import transaction
from django.utils import timezone



class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bank_account = models.JSONField(blank=True, null=True)  # Bank account details as JSONField
    nin = models.CharField(max_length=11, blank=True, null=True)
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
        ('airtime_purchase', 'Airtime Purchase'),  # Airtime purchase type
        ('data_purchase', 'Data Purchase'),  # Data purchase type
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # Additional fields for airtime and data purchase
    status = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)  # Network name (MTN, GLO, etc.)
    unique_element = models.CharField(max_length=20, blank=True, null=True)  # Mobile number
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Data plan for data purchase transactions
    data_plan = models.CharField(max_length=100, blank=True, null=True)  # New field for data plan

    # Add transaction_id field to store the VTPass transaction ID
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # VTPass transaction ID

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username} on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']  # Orders transactions from most recent to oldest


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


class BuyAirtime(models.Model):
    NETWORK_CHOICES = [
        (1, 'MTN'),
        (2, 'GLO'),
        (3, '9MOBILE'),
        (4, 'AIRTEL'),
    ]

    DATA_TYPE_CHOICES = [
        ('VTU', 'VTU'),
        ('Share and Sell', 'Share and Sell'),
    ]

    network = models.IntegerField(choices=NETWORK_CHOICES)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    mobile_number = models.CharField(max_length=11)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of airtime to be bought
    bypass_validator = models.BooleanField(default=False)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='airtime_purchases')
    request_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Add this field
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')], default='failed')
    airtime_response = models.JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.network} - {self.mobile_number} - {self.amount}"

    def process_purchase(self):
        """ Deduct the amount from the user's balance when purchasing airtime """
        if self.amount <= 0:
            raise ValidationError("Amount must be positive.")

        # Ensure user has enough balance
        if self.user.balance < self.amount:
            raise ValidationError("Insufficient balance to complete the purchase.")

        with db_transaction.atomic():
            # Deduct the amount from user's balance
            self.user.balance -= self.amount
            self.user.save()

            # Only return the data to the view, no automatic transaction creation here
            return {
                'user': self.user,
                'amount': self.amount,
                'mobile_number': self.mobile_number,
                'network': self.network,
            }


class BuyData(models.Model):
    NETWORK_CHOICES = [
        (1, 'MTN'),
        (2, 'GLO'),
        (3, '9MOBILE'),
        (4, 'AIRTEL'),
    ]

    DATA_TYPE_CHOICES = [
        ('Glo Data', 'Glo Data'),
        ('Glo SME Data', 'Glo SME Data'),
        ('9mobile Data', '9mobile Data'),
        ('9mobile SME Data', '9mobile SME Data'),
    ]

    network = models.IntegerField(choices=NETWORK_CHOICES)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, blank=True, null=True)
    mobile_number = models.CharField(max_length=11)
    data_plan = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of data to be bought
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='data_purchases')
    request_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Add this field
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')], default='failed')
    data_response = models.JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.network} - {self.mobile_number} - {self.data_plan} - {self.amount}"

    def process_purchase(self):
        """ Deduct the amount from the user's balance when purchasing data """
        if self.amount <= 0:
            raise ValidationError("Amount must be positive.")

        # Ensure user has enough balance
        if self.user.balance < self.amount:
            raise ValidationError("Insufficient balance to complete the purchase.")

        # Start a transaction to ensure atomicity
        self.user.balance -= self.amount  # Deduct the balance directly
        self.user.save()  # Save the user balance deduction
        self.user.refresh_from_db()  # Refresh the user instance to get the updated balance
        return self.user  # Return the user instance after deduction
