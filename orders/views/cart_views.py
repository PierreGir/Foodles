from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.models import Product, Stock
from orders.models import Cart, CartItem
from orders.serializers import CartItemSerializer, CartSerializer


class CartView(APIView):
    def get(self, request, customer_id):
        """
        Retrieve a cart.
        """
        cart = get_object_or_404(Cart, customer_id=customer_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request, customer_id):
        """
        Add a product to a cart or create a new cart.
        """
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        product = get_object_or_404(Product, id=request.data["product_id"])
        quantity = request.data.get("quantity", 1)

        try:
            with transaction.atomic():

                # Get the stock
                stock = Stock.objects.select_for_update().get(
                    product=product, location__name="website"
                )
                if not stock or stock.quantity < quantity:
                    return Response(
                        {
                            "error": "Not enough stock available in the website location."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Deduct the stock
                stock.quantity -= quantity
                stock.save()

                # Add or update the cart item
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=product
                )
                if not created:
                    cart_item.quantity += quantity
                cart_item.save()

                return Response(
                    CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED
                )
        except Stock.DoesNotExist:
            return Response(
                {"error": "Product not available in the website location."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, customer_id):
        """
        Remove a product from cart and return to website.
        """
        cart = get_object_or_404(Cart, customer_id=customer_id)
        product = get_object_or_404(Product, id=request.data["product_id"])
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

        try:
            with transaction.atomic():
                # Get stock
                stock, _ = Stock.objects.select_for_update().get_or_create(
                    product=product, location__name="website"
                )

                # Return the quantity
                stock.quantity += cart_item.quantity
                stock.save()

                # Delete the cart item
                cart_item.delete()

                return Response(
                    {"detail": "Item removed from cart and stock updated."},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except Exception as e:
            return Response(
                {"error": f"Failed to update stock: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
