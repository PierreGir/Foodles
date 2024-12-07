from django.db import models

from .location import Location
from .product import Product


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "location")

    def __str__(self):
        return f"{self.product.name} at {self.location.name}: {self.quantity}"
