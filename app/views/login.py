from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View
from ..models import User
from common.constants import Wrong_info_query_parameter, Wrong_recaptcha_query_parameter


class Login(View):

    def get(self, request):
        try:
            # Check whether the user logged in to the system
            user_id = request.session["user_id"]
            # If the user has already logged in, then redirect it to one of the main windows
            if user_id is not None:
                return redirect("/parts/")

            # If wrong_recaptcha query parameter sent as "true", show a warning on UI
            wrong_recaptcha = request.GET.get(Wrong_recaptcha_query_parameter)
            # If wrong_info query parameter sent as "true", show a warning on UI
            wrong_info = request.GET.get(Wrong_info_query_parameter)
        except Exception as error:
            print("An error occurred while getting the query parameters", error)

        return render(
            request,
            "login/index.html",
            {
                (Wrong_recaptcha_query_parameter): wrong_recaptcha,
                (Wrong_info_query_parameter): wrong_info,
            },
        )

    def post(self, request):
        g_recaptcha_response = request.POST.get("g-recaptcha-response")

        # If the user doesn't click on recaptcha confirmation, then don't allow it to log in
        if g_recaptcha_response == "":
            return redirect("/login?wrong_recaptcha=true")

        email = request.POST.get("email")
        password = request.POST.get("password")
        # Check user information by email first
        user = User.objects.filter(email=email).first()
        # If the user informations don't correct, send a query parameter to display a warning message on UI
        if user is None:
            return redirect("/login?wrong_info=true")

        # Check the entered password by comparing it with the hashed password in DB
        is_user_password_correct = check_password(password, user.password)
        if is_user_password_correct is False:
            return redirect("/login?wrong_info=true")

        # ** User logged in to the system successfully **
        # Store/cache related user's id in session
        request.session["user_id"] = user.id

        if user.team.has_assemble_permission is True:
            # If the user has permission to see and produce the aircrafts, then go to this page as first
            return redirect("/aircrafts/")

        # If the user logs successfully and hasn't permission to see aircraft processes, redirect to the parts page
        return redirect("/parts/")
