from django.shortcuts import render, redirect
from django.contrib.auth import logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from Dashboard.models import CustomUser, FakeLoginAttempt

from django.core.mail import send_mail
import logging
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

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

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 2
LOCKOUT_TIME_MINUTES = 15  # Optional: you can make it reset after a while

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def fake_login(request):
    ip = get_client_ip(request)
    recent_attempts = FakeLoginAttempt.objects.filter(
        ip_address=ip,
        timestamp__gte=timezone.now() - timedelta(minutes=LOCKOUT_TIME_MINUTES)
    )

    if recent_attempts.count() >= MAX_ATTEMPTS:
        return render(request, 'fake_admin_login.html', {
            'locked': True
        })
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Save to DB
        FakeLoginAttempt.objects.create(
            username=username,
            password=password,
            ip_address=ip,
            user_agent=user_agent
        )

        # Log to file
        logger.warning(f"[FAKE ADMIN LOGIN] Username: {username} | Password: {password} | IP: {ip}")

        # Send email
        send_mail(
            subject='🚨 Fake Admin Login Attempt',
            message=f'Username: {username}\nPassword: {password}\nIP: {ip}\nUser Agent: {user_agent}',
            from_email='oduwolesheriff1212@gmail.com',
            recipient_list=['oduwolesheriff1212@gmail.com'],
            fail_silently=True
        )

        return HttpResponse("Invalid username or password.")

    return render(request, 'fake_admin_login.html')

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