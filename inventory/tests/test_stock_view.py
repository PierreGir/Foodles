import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from inventory.models import Location, Product, Stock


@pytest.fixture
def create_stock_data():
    product = Product.objects.create(name="Test Product")
    from_location = Location.objects.create(name="Location 1")
    to_location = Location.objects.create(name="Location 2")
    stock_1 = Stock.objects.create(
        product=product, location=from_location, quantity=100
    )
    stock_2 = Stock.objects.create(product=product, location=to_location, quantity=50)
    return product, from_location, to_location, stock_1, stock_2


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_stocks_all(client, create_stock_data):
    product, from_location, to_location, stock_1, stock_2 = create_stock_data
    url = reverse("get_stock")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "id": 1,
            "quantity": 100,
            "product": {"id": 1, "name": "Test Product"},
            "location": {"id": 1, "name": "Location 1"},
        },
        {
            "id": 2,
            "quantity": 50,
            "product": {"id": 1, "name": "Test Product"},
            "location": {"id": 2, "name": "Location 2"},
        },
    ]


@pytest.mark.django_db
def test_get_stocks_by_location(client, create_stock_data):
    product, from_location, to_location, stock_1, stock_2 = create_stock_data
    url = reverse("get_stock_location", kwargs={"location_id": from_location.id})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "id": 1,
            "quantity": 100,
            "product": {"id": 1, "name": "Test Product"},
            "location": {"id": 1, "name": "Location 1"},
        }
    ]


@pytest.mark.django_db
def test_get_stocks_location_not_found(client):
    url = reverse("get_stock_location", kwargs={"location_id": 9999})

    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "Location not found"}
