# account/urls.py

from django.urls import path
# FIXED: Added 'activate_account' to the import list
from account.views import (
    home,
    login_view,
    register_view,
    password_reset_view,
    password_reset_confirm_view,
    logout_view,
    activate_account
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path("logout/", logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
]