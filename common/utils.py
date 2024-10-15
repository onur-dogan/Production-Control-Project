from django.shortcuts import redirect

# The util function to log out user from the system
def logout(request):
    # Logout user, clear the sessin/cache
    request.session["user_id"] = None

    # Redirect to the login page
    return redirect("/login/")
