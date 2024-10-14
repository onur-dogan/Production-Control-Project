from django.contrib import admin
from django.urls import path
from .views.home import main as home
from .views.login import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('home/', home, name='home')
]