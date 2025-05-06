from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import F
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bank_account = models.JSONField(blank=True, null=True)  # Bank account details as JSONField
    nin = models.CharField(max_length=11, blank=True, null=True)
    bvn = models.CharField(max_length=11, blank=True, null=True, unique=True)  # BVN field added
    referral_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    first_deposit_reward_given = models.BooleanField(default=False)
    has_filled_fund_form = models.BooleanField(default=False)

    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals'
    )

    failed_attempts = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.username

    def deposit(self, amount: float):
        """Method to deposit funds to the user balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        with db_transaction.atomic():
            amount = Decimal(str(amount))  # Always convert to Decimal for safety
            self.balance += amount
            self.save(update_fields=["balance"])

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

    def transfer_referral_bonus_to_balance(self, amount: float):
        """Transfer funds from referral bonus to balance, if bonus meets minimum."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        # Use the value from settings
        min_transfer_amount = Decimal(str(getattr(settings, "MIN_REFERRAL_TRANSFER_AMOUNT", "50.00")))

        if self.referral_bonus < min_transfer_amount:
            raise ValueError(f"Referral bonus must be at least ₦{min_transfer_amount} before you can transfer it.")

        if self.referral_bonus < amount:
            raise ValueError("Insufficient referral bonus for this amount.")

        with db_transaction.atomic():
            amount = Decimal(str(amount))
            self.referral_bonus -= amount
            self.balance += amount
            self.save(update_fields=["referral_bonus", "balance"])

            Transaction.objects.create(
                user=self,
                transaction_type='Bonus To Wallet',
                amount=amount, 
                status='completed'
            )

class MonnifyTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TRANSACTION_TYPES = (
        ('first_deposit', 'First Deposit'),
        ('regular', 'Regular Deposit'),
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        default='regular'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, unique=True)  # your reference
    monnify_transaction_reference = models.CharField(max_length=100, blank=True, null=True)  # returned by Monnify
    bank_code = models.CharField(max_length=10)
    account_number = models.CharField(max_length=20)
    narration = models.CharField(max_length=255, default="User Bonus Withdrawal")
    status = models.CharField(max_length=20, default='pending')  # updated from Monnify response
    currency = models.CharField(max_length=5, default='NGN')
    response_message = models.JSONField(null=True, blank=True)  # optional, for Monnify response
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.user.username} - {self.amount} NGN"

class BankTransfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_code = models.CharField(max_length=10, default='025')
    account_number = models.CharField(max_length=20, default='2417372510')
    status = models.CharField(max_length=20, default='pending')
    reference = models.CharField(max_length=100, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} NGN"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To: {'All Users' if self.user is None else self.user.email} | {self.title}"
    
class FakeLoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} @ {self.timestamp}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('Airtime Purchase', 'Airtime Purchase'),  # Airtime purchase type
        ('Data Purchase', 'Data Purchase'),  # Data purchase type
        ('TV_Subscription', 'TV SUBSCRIPTION'),  # TV SERVICE SUBSCRIPTION
        ('Electricity_Bill', 'Electricity Bill'),  # ElectricityBill Payment
        ('waec_pin_generator', 'WAEC PIN'),
        ('jamb_registration', 'JAMB Registration'),
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
        return "Monnify API Configuration"

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
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

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
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

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



class TVService(models.Model):
    DSTV = 'DSTV'
    GOTV = 'GOTV'
    STARTIMES = 'STARTIMES'
    SHOWMAX = 'SHOWMAX'
    
    TV_CHOICES = [
        (DSTV, 'DStv'),
        (GOTV, 'GOtv'),
        (STARTIMES, 'Startimes'),
        (SHOWMAX, 'Showmax'),
    ]    
    tv_service = models.CharField(
        max_length=10,
        choices=TV_CHOICES,
        default=DSTV,
    )
    data_response = models.JSONField(null=True, blank=True)
    smartcard_number = models.CharField(max_length=100, null=True, blank=True) # Fields for DStv
    iuc_number = models.CharField(max_length=100, null=True, blank=True)  # For GOtv
    # What do you want to do? and Bouquet selection
    action = models.CharField(max_length=100, choices=[
        ('renew', 'Renew Current Bouquet'),
        ('change', 'Change Bouquet'),
    ], null=True, blank=True)

    bouquet = models.CharField(max_length=100, null=True, blank=True)  # Dynamic field for bouquet
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='TV_Subscription')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    startimes_smartcard = models.CharField(max_length=100, null=True, blank=True)  # For Startimes
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates on save

    SHOWMAX_CHOICES = [
        ('full', 'Full - N2,900'),
        ('mobile_only', 'Mobile Only - N1,450'),
        ('sports_full', 'Sports Full - N6,300'),
        ('sports_mobile_only', 'Sports Mobile Only - N3,200'),
    ]
    showmax_type = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        choices=SHOWMAX_CHOICES
    )

    def __str__(self):
        return f"{self.tv_service} Form Submission"

    def process_purchase(self):
        """ Deduct the amount from the user's balance when subscribing on your TV cable """
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


class ElectricityBill(models.Model):
    # Defining the fields based on the form input names and types
    
    serviceID = models.CharField(max_length=255, blank=False, null=False)
    meter_number = models.CharField(max_length=255)
    meter_type = models.CharField(max_length=50, choices=[('Prepaid', 'Prepaid'), ('Postpaid', 'Postpaid')])
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='Electricity_Bill')
    data_response = models.JSONField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Automatically updates on save
    
    def __str__(self):
        return f"Electricity Bill for Meter: {self.meter_number}"
    
    def process_purchase(self):
        """ Deduct the amount from the user's balance when subscribing on your TV cable """
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
    

class WaecPinGenerator(models.Model):
    serviceID = models.CharField(max_length=255, blank=False, null=False)
    ExamType = models.CharField(max_length=50, choices=[('WASSCE/GCE', 'WASSCE/GCE')])
    phone_number = models.CharField(max_length=11)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates on save
    data_response = models.JSONField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='waec_pin_generator', null=True, blank=True)

    def __str__(self):
        return f"{self.ExamType} Pin Generated"
    
    def process_purchase(self):
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
    
class JambRegistration(models.Model):
    serviceID = models.CharField(max_length=255, blank=False, null=False)
    EXAM_TYPE_CHOICES = [
        ('Direct Entry (DE)', 'Direct Entry (DE)'),
        # You can add other exam types here if needed
    ]
    
    exam_type = models.CharField(
        max_length=20, 
        choices=EXAM_TYPE_CHOICES, 
        default='DE'
    )
    jamb_profile_id = models.CharField(
        max_length=50, 
        verbose_name="JAMB Profile ID"
    )
    phone_number = models.CharField(
        max_length=11, 
        verbose_name="Phone Number"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Amount", 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates on save
    data_response = models.JSONField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='jamb_registration', null=True, blank=True)
    
    def __str__(self):
        return f"JAMB Registration - {self.jamb_profile_id} ({self.phone_number})"
    
    class Meta:
        verbose_name = 'JAMB Registration'
        verbose_name_plural = 'JAMB Registrations'
    
    def process_purchase(self):
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