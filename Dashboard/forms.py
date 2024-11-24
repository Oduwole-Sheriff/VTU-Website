from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Added 'bvn' to the list of fields
        fields = ['username', 'password1', 'password2', 'balance', 'bank_account', 'nin', 'bvn', 'is_active', 'is_staff', 'is_superuser']

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
