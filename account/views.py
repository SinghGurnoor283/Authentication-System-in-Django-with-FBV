from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from account.forms import RegistrationForm,PasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .utils import send_activation_email,send_reset_password_email
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from .models import User # Make sure User is imported from models
from django.contrib.auth import authenticate,login

from django.contrib.auth.forms import SetPasswordForm
from account.utils import assign_permission
User = get_user_model()
# Create your views here.
def home(request):
    return render(request, "account/home.html")

# Login
def login_view(request):
    if request.user.is_authenticated:
        # When already authenticated
        if request.user.is_superuser or request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        else:
            return redirect('home')

        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            messages.error(request,"Both fields are required")
            return redirect('login')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"Invalid email or password")
            return redirect('login')
        if not user.is_active:
            messages.error(request,"Your account is not active yet.")
            return redirect('login')
        
        user=authenticate(request,email=email,password=password)
        if user is not None:
            messages.success(request, f"Login attempted with {email}")
            login(request,user)
            if user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_seller:
                return redirect('seller_dashboard')
            else:
                messages.error(request,"You dont have permission to access this area")
                return redirect('home')
        else:
            messages.error(request,"Invalid email or password")
    
    return render(request, "account/login.html")

# Register

def register_view(request):
    print("\n--- CHECKPOINT 1: register_view CALLED ---",flush=True) # New print
    if request.method == "POST":
        print("--- CHECKPOINT 2: POST request received ---",flush=True)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("--- CHECKPOINT 3: Form is valid ---",flush=True)
            # This is a more robust way to save the user
            # It directly calls your custom UserManager
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            city = form.cleaned_data.get('city')
            password = form.cleaned_data.get('password')
            
            # Use your custom manager to create the user
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password
            )
            # Set user to inactive until they activate
            user.is_active = False

            role=request.POST.get("role")
            if role=='seller':
                user.is_seller=True
                user.is_customer=False
            else:
                user.is_seller=False
                user.is_customer=True
            user.save()
            assign_permission(user,role)
            print(f"--- CHECKPOINT 4: User '{user.email}' created in database ---",flush=True) # New print
            # --- The rest of the logic is the same ---
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
           # Instead of manually typing a URL string, this function looks for a URL pattern in your urls.py file that has name="activate".
            #kwargs={...}: It then intelligently inserts the uidb64 and token we just created into the correct placeholders in that URL pattern (<uidb64> and <token>).

            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"

            print("--- CHECKPOINT 5: Activation URL created:", activation_url, "---",flush=True) # New print
            send_activation_email(user, activation_url) 
            messages.success(request, "Registration successful! Please check your email to activate your account.")
            return redirect("login")
        else:
            print("--- ERROR: Form is NOT valid. Errors:", form.errors, "---",flush=True)
            messages.error(request, "Please correct the errors below")
    else:
        form = RegistrationForm()
    return render(request, "account/register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect("home")
# Password Reset (Request reset email)
def password_reset_view(request):
    if request.method == "POST":
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user=User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
                absolute_reset_url = f"{settings.SITE_DOMAIN}{reset_url}"
                messages.success(request,"We have sent u password reset link. Check email")
                send_reset_password_email(user,absolute_reset_url)
        return redirect("login")
    else:
        form=PasswordResetForm()
    return render(request, "account/password_reset.html",{'form':form})

# Password Reset Confirm (Set new password)
def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    

        if not default_token_generator.check_token(user, token):
            messages.error(request,"This links has expired or invalid.")
            return redirect('password_reset')
        if request.method == "POST":
            form=SetPasswordForm(user,request.POST)
            if form.is_valid():

                password1 = request.POST.get("password1")
                password2 = request.POST.get("password2")

                if password1 != password2:
                    messages.error(request, "Passwords do not match.")
                else:
                    form.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect("login")
        else:
            form=SetPasswordForm(user)
        return render(request, "account/password_reset_confirm.html", {"uidb64": uidb64, "token": token})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return redirect('password_reset')
def logout_view(request):
    logout(request)
    return redirect("home")