from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}),
        label='Email Address'
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number'}),
        label='Phone Number'
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Address'}),
        label='Address'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']  # Reordered fields
        labels = {
            'username': 'Username',
            'phone_number': 'Phone Number',
            'address': 'Address'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Your Username'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Your Phone Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter Your Address'})
        }

    def clean_password2(self):
        # Ensure password1 and password2 match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
 
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
#         label='Password'
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']  # Use a custom password field
#         labels = {
#             'username': 'Username',
#             'email': 'Email Address',
#         }
#         widgets = {
#             'username': forms.TextInput(attrs={'placeholder': 'Username'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
#         }

        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']