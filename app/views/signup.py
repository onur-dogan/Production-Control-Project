from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from ..models import Team, User
from ..serializers import TeamSerializer


class SignUp(View):
    def get(self, request):
            # Check whether the user logged in to the system
        user_id = request.session["user_id"]
        # If the user has already logged in, then redirect it to one of the main windows
        if user_id is not None:
            return redirect("/parts/")

        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)

        return render(request, "signup/index.html", {"teams": serializer.data})

    def post(self, request):
        try:
            password = request.POST.get("password")
            confirm_password = request.POST.get("password2")
            # Compare passwords and make sure whether they are same
            if password != confirm_password:
                return HttpResponse("The passwords don't match.")

            email = request.POST.get("email")
            # Check whether any user has already registered to the system before by the same email
            is_user_exist = User.objects.filter(email=email).exists()
            # If the user has already registered to the system before, then go ahead via login page
            if is_user_exist is True:
                return redirect("/login/")

            # Get informations from request body
            team = request.POST.get("team")
            name = request.POST.get("name")
            surname = request.POST.get("surname")

            # Hash the password to store it hashed in DB
            hashed_password = make_password(password)

            # Create a new user model
            new_user = User.objects.create(
                team_id=team,
                name=name,
                surname=surname,
                email=email,
                password=hashed_password,
            )

            # Save new user into the system
            new_user.save()
            # After register processes are done properly, redirect user to the login page to log in to the system
            return redirect("/login/")
        except Exception as error:
            # If any error occurs, return
            print("An error occurred while saving the user", error)

        raise HttpResponse("An error occurred while saving the user. Please try again.")
