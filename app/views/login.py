from django.shortcuts import render, redirect
from django.views import View

class Login(View):

    def get(self, request):
        return render(request, 'login/index.html')
    
    def post(self, request):
        return