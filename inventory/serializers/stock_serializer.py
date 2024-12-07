from rest_framework import serializers

from inventory.models import Stock

from .location_serializer import LocationSerializer
from .product_serializer import ProductSerializer


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    location = LocationSerializer()

    class Meta:
        model = Stock
        fields = ["id", "quantity", "product", "location"]
