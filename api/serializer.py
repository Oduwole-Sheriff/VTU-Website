from rest_framework import serializers
from django.contrib.auth import get_user_model
from Dashboard.models import CustomUser, Transaction

# Use get_user_model() to reference the custom user model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Instead of manually creating a user, use ModelSerializer to take care of user creation.
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User  # This will use the custom user model because we're using get_user_model().
        fields = ['username', 'email', 'password']

    def validate(self, data):
        # Validation to check if username or email already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already taken.')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email is already taken.')

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    # Serializer for CustomUser model to include the balance and other necessary fields
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'balance']


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        # Ensure that deposit amount is positive
        if value <= 0:
            raise serializers.ValidationError("Deposit amount must be greater than 0.")
        return value


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


class TransactionSerializer(serializers.ModelSerializer):
    # Serializer to handle transactions. 
    # Recipient can be null for deposit and withdrawal transactions.
    recipient = CustomUserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'timestamp', 'recipient']
        read_only_fields = ['id', 'timestamp', 'recipient']


        

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