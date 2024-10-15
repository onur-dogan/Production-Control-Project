from django.shortcuts import redirect
from app.models import Part_stock_status
from .constants import Increase, Decrease


# The util function to log out user from the system
def logout(request):
    # Logout user, clear the sessin/cache
    request.session["user_id"] = None

    # Redirect to the login page
    return redirect("/login/")


# Retrieve stock status according to the parameter
def getStockPartStatus(increase=True):
    return Part_stock_status.objects.filter(
        name__icontains=Increase if increase else Decrease
    ).first()
