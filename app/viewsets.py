from .models import (
    Team,
    Aircraft,
    Aircraft_production,
    Part,
    Part_stock,
    Part_stock_mobility,
    Part_stock_status,
    User,
)
from .serializers import (
    TeamSerializer,
    UserSerializer,
    AircraftProductionSerializer,
    PartSerializer,
    AircraftSerializer,
    PartStockSerializer,
    PartStockStatusSerializer,
    PartStockMobilitySerializer,
)
from rest_framework import viewsets


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teams to be viewed or edited.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows aircrafts to be viewed or edited.
    """

    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AircraftProductionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows aircraft productions to be viewed or edited.
    """

    queryset = Aircraft_production.objects.all()
    serializer_class = AircraftProductionSerializer

class PartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows parts to be viewed or edited.
    """

    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartStockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows part stocks to be viewed or edited.
    """

    queryset = Part_stock.objects.all()
    serializer_class = PartStockSerializer

class PartStockStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows part stock statuses to be viewed or edited.
    """

    queryset = Part_stock_status.objects.all()
    serializer_class = PartStockStatusSerializer

class PartStockMobilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows part stock statuses to be viewed or edited.
    """

    queryset = Part_stock_mobility.objects.all()
    serializer_class = PartStockMobilitySerializer
