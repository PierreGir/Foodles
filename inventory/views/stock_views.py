from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import Location, Stock
from inventory.serializers.stock_serializer import StockSerializer


class StockView(APIView):
    def get(self, request, location_id=None):
        if location_id:
            try:
                location = Location.objects.get(pk=location_id)
            except Location.DoesNotExist:
                return Response(
                    {"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND
                )
            stocks = Stock.objects.filter(location=location)
        else:
            stocks = Stock.objects.all()

        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
