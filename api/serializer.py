from rest_framework import serializers
from django.contrib.auth import get_user_model
from Dashboard.models import CustomUser, BankTransfer, MonnifyTransaction, PaystackTransaction, Transaction, BuyAirtime, BuyData, TVService, ElectricityBill, WaecPinGenerator, JambRegistration
from authentication.models import Profile
from django.contrib.auth.password_validation import validate_password
from django.db import transaction as db_transaction
from decimal import Decimal

# Use get_user_model() to reference the custom user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    referral_code = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2', 'referral_code', 'referral_bonus']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already taken.')

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email is already taken.')

        try:
            validate_password(data['password1'])
        except Exception as e:
            raise serializers.ValidationError(f"Password error: {str(e)}")

        return data

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        address = validated_data.pop('address', None)
        referral_code = validated_data.pop('referral_code', None)

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password1'])

        # Handle referral logic here
        if referral_code:
            try:
                referrer = User.objects.get(username=referral_code)
                user.referred_by = referrer  # Only works if this field exists on your CustomUser
                user.save()

            except User.DoesNotExist:
                pass  # You can optionally raise a warning

        user.save()

        # Create or update user profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'phone_number': phone_number, 'address': address}
        )

        if not created:
            profile.phone_number = phone_number or profile.phone_number
            profile.address = address or profile.address
            profile.save()

        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    dob = serializers.DateField(required=False)
    document_type = serializers.ChoiceField(choices=[('nin', 'National Identification Number (NIN)'), ('bvn', 'Bank Verification Number (BVN)')])
    nin = serializers.CharField(max_length=11, required=False, allow_blank=True)
    bvn = serializers.CharField(max_length=11, required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'dob', 'document_type', 'nin', 'bvn']

    def validate(self, data):
        # Ensure that nin or bvn is provided based on the selected document_type
        if data['document_type'] == 'nin' and not data.get('nin'):
            raise serializers.ValidationError("NIN is required for the selected identity type.")
        elif data['document_type'] == 'bvn' and not data.get('bvn'):
            raise serializers.ValidationError("BVN is required for the selected identity type.")

        # Check if the BVN already exists (except for the current user)
        bvn = data.get('bvn')
        if bvn and CustomUser.objects.filter(bvn=bvn).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("The BVN already exists for another user.")

        return data

    def update(self, instance, validated_data):
        # Update the user model
        instance.nin = validated_data.get('nin', instance.nin)
        instance.bvn = validated_data.get('bvn', instance.bvn)
        instance.save()

        # Update the associated profile with full_name and dob
        profile = instance.profile  # Assuming a 1-to-1 relationship exists between User and Profile
        profile.full_name = validated_data.get('full_name', profile.full_name)
        profile.dob = validated_data.get('dob', profile.dob)
        profile.save()

        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    # Serializer for CustomUser model to include the balance and other necessary fields
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'balance', 'bonus']


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        # Ensure withdrawal amount is positive
        if value <= 0:
            raise serializers.ValidationError("Withdrawal amount must be greater than 0.")
        return value


class TransferSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        # Ensure transfer amount is positive
        if value <= 0:
            raise serializers.ValidationError("Transfer amount must be greater than 0.")
        return value

    def validate_recipient_id(self, value):
        # Ensure the recipient exists
        try:
            recipient = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Recipient does not exist.")
        return value


class MonnifyTransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # or use PrimaryKeyRelatedField if needed

    class Meta:
        model = MonnifyTransaction
        fields = [
            'id',
            'user',
            'amount',
            'payment_reference',
            'monnify_transaction_reference',
            'bank_code',
            'account_number',
            'narration',
            'status',
            'currency',
            'response_message',
            'date'
        ]
        read_only_fields = ['status', 'monnify_transaction_reference', 'response_message', 'date']


class BankTransferSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BankTransfer
        fields = [
            'id',
            'user',
            'amount',
            'bank_code',
            'account_number',
            'status',
            'reference',
            'created_at'
        ]
        read_only_fields = ['status', 'created_at']

class PaystackTransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PaystackTransaction
        fields = [
            'id',
            'user_email',
            'transaction_type',
            'reference',
            'amount',
            'payment_method',
            'status',
            'currency',
            'paid_at',
            'created_at',
            'response_message'
        ]
        read_only_fields = fields  # Make it read-only if you're not accepting POST requests

class TransactionSerializer(serializers.ModelSerializer):
    # Serialize additional fields
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'timestamp', 'recipient', 'status', 'product_name', 'unique_element', 'unit_price']
        read_only_fields = ['id', 'timestamp', 'recipient']


class BuyAirtimeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    # Calculate the remaining balance after airtime purchase (read-only field)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BuyAirtime
        fields = ['id', 'user', 'network', 'data_type', 'mobile_number', 'amount', 'bypass_validator', 'remaining_balance', 'airtime_response', 'transaction_id']

    def create(self, validated_data):
        """Override the create method to create the BuyAirtime instance without balance deduction"""
        # Create the BuyAirtime instance
        buy_airtime = BuyAirtime.objects.create(**validated_data)
        return buy_airtime


class BuyDataSerializer(serializers.ModelSerializer):
    network = serializers.ChoiceField(choices=BuyData.NETWORK_CHOICES)
    data_type = serializers.ChoiceField(choices=BuyData.DATA_TYPE_CHOICES, allow_blank=True, required=False)
    mobile_number = serializers.CharField(max_length=11)
    data_plan = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    request_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=[('success', 'Success'), ('failed', 'Failed')], default='failed')
    data_response = serializers.JSONField(required=False, allow_null=True)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)
    transaction_id = serializers.CharField(max_length=255, required=False, allow_blank=True)

    # Calculate the remaining balance after airtime purchase (read-only field)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = BuyData
        fields = '__all__'

    def create(self, validated_data):
        """
        Override create method to handle data purchase and transaction creation.
        We will remove the balance deduction here since it's handled in the view.
        """
        # Simply create the BuyData instance and return
        buy_data_instance = BuyData.objects.create(**validated_data)
        return buy_data_instance


class TVServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVService
        fields = [
            'tv_service',
            'smartcard_number',
            'iuc_number',
            'action',
            'bouquet',
            'phone_number',
            'amount',
            'startimes_smartcard',
            'showmax_type',
            'data_response'
        ]

    def create(self, validated_data):
        """Override the create method to add the user to the validated data"""
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Add the user to the validated data
        
        # Create and return the TVService instance
        tv_service = TVService.objects.create(**validated_data)
        return tv_service


class ElectricityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityBill
        fields = [
            'serviceID',
            'meter_number',
            'meter_type',
            'phone_number',
            'amount',
            'data_response'
        ]

    def create(self, validated_data):
        """Override the create method to add the user to the validated data"""
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Add the user to the validated data
        
        # Create and return the TVService instance
        Electricity_Bill = ElectricityBill.objects.create(**validated_data)
        return Electricity_Bill


class WaecPinGeneratorSerializer(serializers.ModelSerializer):
    serviceID = serializers.CharField(max_length=255)
    ExamType = serializers.ChoiceField(choices=[('WASSCE/GCE', 'WASSCE/GCE')])
    phone_number = serializers.CharField(max_length=11)
    quantity = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    request_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    transaction_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    data_response = serializers.JSONField(required=False, allow_null=True)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)

    # Calculate the remaining balance after pin generation (read-only field)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = WaecPinGenerator
        fields = '__all__'

    def create(self, validated_data):
        """Override the create method to add the user to the validated data"""
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Add the user to the validated data
        
        # Create and return the WaecPinGenerator instance
        waec_pin_generator = WaecPinGenerator.objects.create(**validated_data)
        return waec_pin_generator



class JambRegistrationSerializer(serializers.ModelSerializer):
    # This is used for representing the related CustomUser model
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = JambRegistration
        fields = [
            'user',
            'serviceID',
            'exam_type',
            'jamb_profile_id',
            'phone_number',
            'amount',
            'data_response',
        ] # This includes all fields from the model
        read_only_fields = ['created_at', 'updated_at', 'transaction_id', 'user']  # Fields that should be read-only

    def create(self, validated_data):
        """Override the create method to add the user to the validated data"""
        user = self.context['request'].user  # Get the user from the request context
        validated_data['user'] = user  # Add the user to the validated data

        jamb_registration = JambRegistration.objects.create(**validated_data)
        return jamb_registration

# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ['user', 'balance']

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ['user', 'wallet', 'transaction_type', 'amount', 'created_at']


# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = "__all__"

#     def validate_name(self, value):
#         if self.instance: 
#             existing_post = Post.objects.exclude(pk=self.instance.pk).filter(name=value)
#             if existing_post.exists():
#                 raise serializers.ValidationError("A post with this name already exists.")
#         else:
#             if Post.objects.filter(name=value).exists():
#                 raise serializers.ValidationError("A post with this name already exists.")
#         return value

    # def create(self, validated_data):
    #     return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.save()
    #     return instance

# class PersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['city'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entry
#         fields = '__all__'

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'