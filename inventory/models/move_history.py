from django.db import models

from .location import Location
from .stock import Product


class MoveHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_location = models.ForeignKey(
        Location, related_name="from_location", on_delete=models.CASCADE
    )
    to_location = models.ForeignKey(
        Location, related_name="to_location", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move {self.quantity} of {self.stock.product.name} from {self.from_location.name} to {self.to_location.name} at {self.timestamp}"
