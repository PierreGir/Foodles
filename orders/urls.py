from django.urls import path

from .views import CartView

urlpatterns = [
    path("cart/<int:customer_id>/", CartView.as_view(), name="cart"),
]
