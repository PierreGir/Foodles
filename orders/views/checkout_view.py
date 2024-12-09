from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Cart, CartItem, Order, OrderItem
from orders.services.payment_service import PaymentService


class CheckoutView(APIView):
    def post(self, request, customer_id):
        """
        Process checkout
        """
        cart = get_object_or_404(Cart, customer_id=customer_id)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Compute total price
        total_price = 0
        try:
            with transaction.atomic():
                for item in cart_items.select_related("product"):
                    total_price += item.quantity * item.product.price

                # Process payment
                payment_response = PaymentService.process_payment(
                    total_price, customer_id
                )
                if not payment_response.get("success", False):
                    raise Exception("Payment processing failed")

                # Create order
                order = Order.objects.create(
                    customer=cart.customer, total_price=total_price, status="completed"
                )
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order, product=item.product, quantity=item.quantity
                    )

                # Clear the cart
                cart_items.delete()

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"detail": "Checkout completed successfully", "order_id": order.id},
            status=status.HTTP_200_OK,
        )
