from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user and retrieve cleaned data for phone_number and address
            user = form.save()  # This saves the user
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')
            
            # Create a Profile instance for the user
            Profile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address
            )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created {username}! You can now log in.')
            return redirect('login')  # Redirect to the login page after success

    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, "profile.html", context)

