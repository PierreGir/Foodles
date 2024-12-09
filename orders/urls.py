from django.urls import path

from orders.views.cart_views import CartView
from orders.views.checkout_view import CheckoutView

urlpatterns = [
    path("cart/<int:customer_id>/", CartView.as_view(), name="cart"),
    path('checkout/<int:customer_id>/', CheckoutView.as_view(), name='checkout'),
]
