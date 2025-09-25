from django.shortcuts import render
from account.decorators import login_and_role_required

# Create your views here.
@login_and_role_required('seller')
def seller_dashboard_view(req):
    return render(req,'seller/dashboard.html')