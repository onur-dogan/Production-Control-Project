from rest_framework import serializers
from .models import (
    Team,
    User,
    Aircraft,
    Aircraft_production,
    Part,
    Part_stock,
    Part_stock_mobility,
    Part_stock_status,
)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "has_assemble_permission", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "surname",
            "email",
            "password",
            "is_active",
            "created_at",
            "latest_login",
        ]


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["id", "name", "description", "is_active", "created_at", "updated_at"]


class AircraftProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft_production
        fields = [
            "id",
            "product_no",
            "aircraft",
            "used_parts",
            "is_completed",
            "is_canceled",
            "user",
            "created_at",
            "updated_at",
        ]


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [
            "id",
            "name",
            "description",
            "team",
            "aircraft",
            "is_active",
            "created_at",
            "updated_at",
        ]


class PartStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part_stock
        fields = ["id", "part", "count", "updated_at"]


class PartStockStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part_stock_status
        fields = ["id", "name", "created_at"]


class PartStockMobilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Part_stock_mobility
        fields = [
            "id",
            "aircraft_production",
            "part",
            "status",
            "description",
            "user",
            "created_at",
        ]
