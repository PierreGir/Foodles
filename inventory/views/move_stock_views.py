from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import Location, MoveHistory, Product, Stock
from inventory.serializers.move_stock_serializer import MoveStockSerializer


class MoveStockView(APIView):
    def post(self, request):
        serializer = MoveStockSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "errors": [
                        str(error)
                        for errors in serializer.errors.values()
                        for error in errors
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        product = Product.objects.get(pk=data["product_id"])
        from_location = Location.objects.get(pk=data["from_location_id"])
        to_location = Location.objects.get(pk=data["to_location_id"])

        # Update stock
        from_stock = Stock.objects.get(product=product, location=from_location)
        from_stock.quantity -= data["quantity"]
        from_stock.save()

        to_stock, _ = Stock.objects.get_or_create(product=product, location=to_location)
        to_stock.quantity += data["quantity"]
        to_stock.save()

        # Log movement
        MoveHistory.objects.create(
            product=product,
            from_location=from_location,
            to_location=to_location,
            quantity=data["quantity"],
        )

        return Response(
            {
                "message": f"Moved {data['quantity']} of {product.name} from {from_location.name} to {to_location.name}"
            },
            status=status.HTTP_200_OK,
        )
