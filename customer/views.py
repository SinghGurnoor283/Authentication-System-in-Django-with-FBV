from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from account.decorators import login_and_role_required
# Create your views here.
@login_and_role_required('customer')
def customer_dashboard_view(request):
    
    return render(request, "customer/dashboard.html")

@login_and_role_required('customer')
def password_change_view(request):
    """Change Password"""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user)  # keep user logged in after password change
            logout(request)
            messages.success(request, "Your password has been updated successfully.Please Log in Again. ")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "customer/password_change.html")