from django.urls import path
from customer.views import password_change_view,customer_dashboard_view
urlpatterns = [
    path('dashboard/',customer_dashboard_view,name='customer_dashboard'),
    path('password-change/',password_change_view,name='password_change')
]
