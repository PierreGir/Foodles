from django.db import models

from orders.models import Customer


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="carts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.customer.name}"
