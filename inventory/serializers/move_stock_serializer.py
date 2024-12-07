from rest_framework import serializers

from inventory.models import Location, Product, Stock


class MoveStockSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    from_location_id = serializers.IntegerField()
    to_location_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        product = Product.objects.filter(pk=data["product_id"]).first()
        if not product:
            raise serializers.ValidationError("Invalid product ID.")

        from_location = Location.objects.filter(pk=data["from_location_id"]).first()
        if not from_location:
            raise serializers.ValidationError("Invalid source location ID.")

        to_location = Location.objects.filter(pk=data["to_location_id"]).first()
        if not to_location:
            raise serializers.ValidationError("Invalid destination location ID.")

        stock = Stock.objects.filter(product=product, location=from_location).first()
        if not stock or stock.quantity < data["quantity"]:
            raise serializers.ValidationError(
                "Insufficient stock at the source location."
            )

        existing_stock_at_to_location = Stock.objects.filter(
            location=to_location
        ).first()
        if (
            existing_stock_at_to_location
            and existing_stock_at_to_location.product != product
        ):
            raise serializers.ValidationError(
                "The destination location already contains a different product."
            )

        return data
