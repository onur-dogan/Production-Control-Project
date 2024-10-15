from django.contrib import admin
from django.urls import path
from .views.login import Login
from .views.signup import SignUp
from .views.parts import Parts, PartListView
from .views.aircrafts import Aircrafts, AircraftListView, AircraftProductionListView
from common.utils import logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('parts/', Parts.as_view(), name='parts'),
    path('partsData/', PartListView.as_view(), name='partsData'),
    path('aircrafts/', Aircrafts.as_view(), name='aircrafts'),
    path('aircraftsData/', AircraftListView.as_view(), name='aircraftsData'),
    path('aircraftProductionsData/', AircraftProductionListView.as_view(), name='aircraftProductionsData'),
]