from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}),
        label='Email Address'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Custom password field
        labels = {
            'username': 'Username',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Your Name'}),
        }

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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']