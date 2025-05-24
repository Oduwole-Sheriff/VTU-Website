from django import forms
from .models import CustomUser, Notification, BuyAirtime, BuyData, TVService, ElectricityBill, WaecPinGenerator, JambRegistration
from django.core.exceptions import ValidationError
from django.conf import settings
from decimal import Decimal, InvalidOperation
import json

class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    # Treat bank_account as plain text in admin
    bank_account = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label="Bank Account (JSON)"
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password1', 'password2',
            'balance', 'bonus', 'bank_account',
            'nin', 'bvn', 'is_active', 'is_staff', 'is_superuser'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and isinstance(instance.bank_account, dict):
            self.initial['bank_account'] = json.dumps(instance.bank_account, indent=2)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        bvn = cleaned_data.get("bvn")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        if bvn and len(bvn) != 11:
            raise forms.ValidationError("BVN must be 11 digits long.")

        return cleaned_data

    def clean_bank_account(self):
        data = self.cleaned_data.get("bank_account")
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Bank account must be valid JSON.")
        return {}

        
class NINForm(forms.Form):
    nin = forms.CharField(max_length=11, label='Enter your NIN')

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')
        # Optionally validate the NIN format (you can adjust this regex to fit your needs)
        if len(nin) != 11:  # Assuming the NIN is 20 digits long
            raise forms.ValidationError('NIN should be 11 characters long.')
        return nin
    
class BankTransferForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01, # Add min_value validation here too
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bank_code = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    account_number = forms.CharField(
        max_length=10, # Standard NGN account number length
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    reference = forms.CharField(max_length=100, widget=forms.HiddenInput())

class ReferralBonusTransferForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount to transfer'})
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if self.user is None:
            raise forms.ValidationError("User context is required.")

        try:
            min_amount = Decimal(str(getattr(settings, "MIN_REFERRAL_TRANSFER_AMOUNT", "50.00")))
        except InvalidOperation:
            raise forms.ValidationError("Invalid setting for minimum referral transfer amount.")

        # Check if user's referral bonus is at least the minimum
        if self.user.referral_bonus < min_amount:
            raise forms.ValidationError(f"Referral bonus must be at least ₦{min_amount} before transferring.")

        # Check if the entered amount is less than the minimum allowed
        if amount < min_amount:
            raise forms.ValidationError(f"You cannot transfer less than ₦{min_amount}.")

        # Check if user has enough bonus for the requested transfer
        if self.user.referral_bonus < amount:
            raise forms.ValidationError("Insufficient referral bonus for this amount.")

        return amount


class NotificationForm(forms.ModelForm):
    send_to_all = forms.BooleanField(required=False, initial=False, label="Send to all users")

    class Meta:
        model = Notification
        fields = ['title', 'message', 'user', 'send_to_all']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        send_to_all = cleaned_data.get("send_to_all")
        user = cleaned_data.get("user")

        if send_to_all:
            cleaned_data['user'] = None  # Clear the user field if sending to all
        elif not user:
            raise forms.ValidationError("Please select a user or check 'Send to all users'.")

        return cleaned_data


class BuyAirtimeForm(forms.ModelForm):
    class Meta:
        model = BuyAirtime
        fields = ['network', 'data_type', 'mobile_number', 'amount', 'bypass_validator']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'maxlength': '11', 'minlength': '11', 'type': 'tel', 'placeholder': ''}),
            'amount': forms.NumberInput(attrs={'min': '2', 'maxlength': '11', 'type': 'text', 'placeholder': ''}),
            'network': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'network-name', 'name': 'network', 'type': 'text', 'placeholder': ''}),  # Disable the Select field
            'data_type': forms.Select(attrs={'id': '', 'name': 'data_type'}),
            'bypass_validator': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    # Don't require the user field in the form (we will set it manually)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user  # Set the user field manually


class BuyDataForm(forms.ModelForm):
    class Meta:
        model = BuyData
        fields = ['network', 'data_type', 'mobile_number', 'data_plan', 'amount']

    # Custom validation for mobile number to check the length
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if len(mobile_number) != 11:
            raise ValidationError("Mobile number must be 11 digits long.")
        return mobile_number

    # You can add custom clean methods for other fields if necessary, for example:
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Amount must be positive.")
        return amount

    # Custom method to validate if the selected network and data type match
    def clean(self):
        cleaned_data = super().clean()
        network = cleaned_data.get('network')
        data_type = cleaned_data.get('data_type')

        # If the network is Glo or 9Mobile, data_type must be selected
        if network in [2, 3]:  # Glo or 9Mobile
            if not data_type:
                raise ValidationError('Please select a data type for the selected network.')

        return cleaned_data

    # You can add a method to dynamically handle the available data types based on the network
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide data_type field initially if network is not Glo or 9mobile
        if self.instance and self.instance.network not in [2, 3]:
            self.fields['data_type'].widget = forms.HiddenInput()
        elif self.instance and self.instance.network == 2:  # Glo
            self.fields['data_type'].queryset = BuyData.DATA_TYPE_CHOICES[:2]  # Glo Data types
        elif self.instance and self.instance.network == 3:  # 9mobile
            self.fields['data_type'].queryset = BuyData.DATA_TYPE_CHOICES[2:]  # 9mobile Data types
        else:
            self.fields['data_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        # You can override the save method to add custom logic if needed
        # For instance, adding additional fields or setting default values
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class TVServiceForm(forms.ModelForm):
    class Meta:
        model = TVService
        fields = ['tv_service', 'smartcard_number', 'iuc_number', 'action', 'bouquet', 'phone_number', 'amount', 'startimes_smartcard', 'showmax_type']

    def clean(self):
        cleaned_data = super().clean()
        
        # Get the user instance from the request (assuming the user is logged in)
        user = self.instance.user

        # Check if the amount is valid and if the user has sufficient balance
        amount = cleaned_data.get('amount')

        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        if amount is not None and user.balance < amount:
            raise ValidationError("Insufficient balance to complete the purchase.")
        
        return cleaned_data


class ElectricityBillForm(forms.ModelForm):
    class Meta:
        model = ElectricityBill
        fields = ['serviceID', 'meter_number', 'meter_type', 'phone_number', 'amount']
        widgets = {
            'serviceID': forms.TextInput(attrs={'id': 'serviceID', 'readonly': 'readonly', 'type': 'text', 'placeholder': ''}),
            'meter_number': forms.TextInput(attrs={'id':'meter_number','placeholder': ' ', 'type': 'text',}),
            'phone_number': forms.TextInput(attrs={'placeholder': ' ', 'type': 'text'}),
            'amount': forms.NumberInput(attrs={'placeholder': ' ', 'type': 'tel'}),
            'meter_type': forms.Select(attrs={'id': 'meter-type'})
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


class WaecPinGeneratorForm(forms.ModelForm):
    class Meta:
        model = WaecPinGenerator
        fields = ['serviceID', 'ExamType', 'phone_number', 'quantity', 'amount']

        widgets = {
            'serviceID': forms.HiddenInput(),
            'ExamType': forms.Select(
                choices=[('', 'Please Select ExamType'), ('WASSCE/GCE', 'WASSCE/GCE')],
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Enter Phone Number', 'maxlength': '11', 'minlength': '11'}
            ),
            'quantity': forms.NumberInput(
                attrs={'placeholder': 'Enter Quantity', 'min': '1', 'max': '10', 'value': '1'}
            ),
            'amount': forms.TextInput(
                attrs={'placeholder': 'Enter Amount', 'id': 'amountField', 'maxlength': '11', 'minlength': '2', 'disabled': 'disabled'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(WaecPinGeneratorForm, self).__init__(*args, **kwargs)
        # Set the initial value to '' to keep "Please Select ExamType" as the selected value by default
        self.fields['ExamType'].initial = ''

        # Make the first option ("Please Select ExamType") disabled
        self.fields['ExamType'].widget.choices = [
            ('', 'Please Select ExamType'),
            ('WASSCE/GCE', 'WASSCE/GCE')
        ]
        

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

class JambRegistrationForm(forms.ModelForm):
    class Meta:
        model = JambRegistration
        fields = ['serviceID', 'exam_type', 'jamb_profile_id', 'phone_number', 'amount']
        widgets = {
            'serviceID': forms.HiddenInput(),
            'jamb_profile_id': forms.TextInput(attrs={'placeholder': 'Enter JAMB Profile ID', 'id': 'id_jamb_profile_id'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'maxlength': '11'}),
            'amount': forms.TextInput(attrs={'placeholder': 'Enter Amount', 'id': 'amountField', 'disabled': 'disabled'})
        }

    def __init__(self, *args, **kwargs):
        super(JambRegistrationForm, self).__init__(*args, **kwargs)
        
        # Set the initial value to '' to keep "Please Select Exam Type" as the selected value by default
        self.fields['exam_type'].initial = ''
        
        # Modify the choices to include the disabled "Please Select Exam Type" option
        self.fields['exam_type'].widget.choices = [
            ('', 'Please Select Exam Type'),  # Disabled by default
            ('Direct Entry (DE)', 'Direct Entry (DE)'),
            # Add more exam types here if necessary
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise forms.ValidationError("Phone number must be 11 digits.")
        return phone_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            raise forms.ValidationError("Amount is required.")
        return amount