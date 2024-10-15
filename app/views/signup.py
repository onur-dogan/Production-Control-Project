from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from ..models import Team, User
from ..serializers import TeamSerializer
from ..forms import UserForm


class SignUp(View):
    def get(self, request):
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

            new_user = UserForm(request.POST)

            if new_user.is_valid():
                new_user.save()
                return redirect("/login/")
        except Exception as error:
            # If any error occurs, return
            print("An error occurred while saving the user", error)

        raise HttpResponse("An error occurred while saving the user. Please try again.")
