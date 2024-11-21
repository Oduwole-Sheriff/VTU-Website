from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Removed 'first_name' and 'last_name' from the fields
        fields = ['username', 'password1', 'password2', 'balance', 'bank_account', 'nin', 'is_active', 'is_staff', 'is_superuser']  

    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Add the bank_account queryset if the field is part of the form
    #     if 'bank_account' in self.fields:
    #         # If the user already has a bank account, set it as read-only or limit selection to their existing account
    #         if self.instance and self.instance.bank_account:
    #             self.fields['bank_account'].queryset = BankAccount.objects.filter(user=self.instance)
    #             self.fields['bank_account'].widget.attrs['readonly'] = True  # Make the bank_account field read-only
    #         else:
    #             # For new users, allow selecting any bank account (or leave this open for manual creation)
    #             self.fields['bank_account'].queryset = BankAccount.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class NINForm(forms.Form):
    nin = forms.CharField(max_length=11, label='Enter your NIN')

    def clean_nin(self):
        nin = self.cleaned_data.get('nin')
        # Optionally validate the NIN format (you can adjust this regex to fit your needs)
        if len(nin) != 11:  # Assuming the NIN is 20 digits long
            raise forms.ValidationError('NIN should be 11 characters long.')
        return nin
