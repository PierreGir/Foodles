from django.urls import path

from inventory.views.move_stock_views import MoveStockView
from inventory.views.stock_views import StockView

urlpatterns = [
    path("stock/", StockView.as_view(), name="get_stock"),
    path("stock/<int:location_id>/", StockView.as_view(), name="get_stock_location"),
    path("move/", MoveStockView.as_view(), name="move_stock"),
]
