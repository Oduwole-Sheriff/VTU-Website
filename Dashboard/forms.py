from django import forms
from .models import CustomUser, BuyAirtime, BuyData, TVService, ElectricityBill, WaecPinGenerator, JambRegistration
from django.core.exceptions import ValidationError

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Added 'bvn' to the list of fields
        fields = ['username', 'password1', 'password2', 'balance', 'bonus', 'bank_account', 'nin', 'bvn', 'is_active', 'is_staff', 'is_superuser']

    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    bvn = forms.CharField(
        max_length=11,  # BVN is typically 11 digits long
        widget=forms.TextInput(attrs={'placeholder': 'Enter your BVN'}),
        label="BVN"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        # Validate BVN format
        bvn = cleaned_data.get('bvn')
        if bvn and len(bvn) != 11:
            raise forms.ValidationError("BVN must be 11 digits long.")

        return cleaned_data

class NINForm(forms.Form):
    nin = forms.CharField(max_length=11, label='Enter your NIN')

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')
        # Optionally validate the NIN format (you can adjust this regex to fit your needs)
        if len(nin) != 11:  # Assuming the NIN is 20 digits long
            raise forms.ValidationError('NIN should be 11 characters long.')
        return nin

class BuyAirtimeForm(forms.ModelForm):
    class Meta:
        model = BuyAirtime
        fields = ['network', 'data_type', 'mobile_number', 'amount', 'bypass_validator']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'maxlength': '11', 'minlength': '11'}),
            'amount': forms.NumberInput(attrs={'min': '2', 'maxlength': '11'}),
            'network': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'network-name', 'name': 'network'}),  # Disable the Select field
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
            'serviceID': forms.TextInput(attrs={'id': 'serviceID', 'readonly': 'readonly'}),
            'meter_number': forms.TextInput(attrs={'id':'meter_number','placeholder': 'Verify Your Meter Number'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Mobile Number'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Amount'}),
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