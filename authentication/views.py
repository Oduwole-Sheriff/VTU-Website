from django.shortcuts import render, redirect
from django.contrib.auth import logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from Dashboard.models import CustomUser

# Create your views here.

def register(request):
    referral_code = request.GET.get('referral')  # get referral from URL

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')

            # If referral code was in POST (hidden input), assign referred_by
            referral_username = request.POST.get('referral_code')
            if referral_username:
                try:
                    referrer = CustomUser.objects.get(username=referral_username)
                    user.referred_by = referrer
                    user.save()

                    # Give the referrer a bonus
                    referrer.bonus += 5.00
                    referrer.save()
                except CustomUser.DoesNotExist:
                    pass  # Ignore invalid referral

            # Create user profile
            Profile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address
            )

            messages.success(request, f'Your account has been created {user.username}! You can now log in.')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'referral_code': referral_code  # Pass to the template
    })


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

def custom_logout(request):
    # Save the form_submitted state before logging out
    form_submitted = request.session.get('form_submitted', False)
    
    # Log the user out
    logout(request)
    
    # Re-set the form_submitted flag
    if form_submitted:
        request.session['form_submitted'] = True
    
    # Redirect to the home page or login page after logout
    return redirect('home-page')  # You can change this to whatever page you want to redirect to after logout