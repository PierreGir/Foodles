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
def test_move_stock_success(client, create_stock_data):
    product, from_location, to_location, stock_1, stock_2 = create_stock_data
    url = reverse("move_stock")
    data = {
        "product_id": product.id,
        "from_location_id": from_location.id,
        "to_location_id": to_location.id,
        "quantity": 50,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "message": "Moved 50 of Test Product from Location 1 to Location 2"
    }

    stock_1.refresh_from_db()
    stock_2.refresh_from_db()

    assert stock_1.quantity == 50
    assert stock_2.quantity == 100


@pytest.mark.django_db
def test_move_stock_invalid_product(client, create_stock_data):
    _, from_location, to_location, _, _ = create_stock_data
    url = reverse("move_stock")
    data = {
        "product_id": 9999,  # Invalid product ID
        "from_location_id": from_location.id,
        "to_location_id": to_location.id,
        "quantity": 50,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"errors": ["Invalid product ID."]}


@pytest.mark.django_db
def test_move_stock_invalid_location(client, create_stock_data):
    product, _, to_location, _, _ = create_stock_data
    url = reverse("move_stock")
    data = {
        "product_id": product.id,
        "from_location_id": 9999,
        "to_location_id": to_location.id,
        "quantity": 50,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"errors": ["Invalid source location ID."]}


@pytest.mark.django_db
def test_move_stock_insufficient_stock(client, create_stock_data):
    product, from_location, to_location, stock_1, _ = create_stock_data
    url = reverse("move_stock")
    data = {
        "product_id": product.id,
        "from_location_id": from_location.id,
        "to_location_id": to_location.id,
        "quantity": 200,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"errors": ["Insufficient stock at the source location."]}


@pytest.mark.django_db
def test_move_stock_conflicting_product(client, create_stock_data):
    product, from_location, to_location, _, _ = create_stock_data
    conflicting_product = Product.objects.create(name="Conflicting Product")
    Stock.objects.filter(location=to_location).delete()
    Stock.objects.create(
        product=conflicting_product, location=to_location, quantity=100
    )

    url = reverse("move_stock")
    data = {
        "product_id": product.id,
        "from_location_id": from_location.id,
        "to_location_id": to_location.id,
        "quantity": 50,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "errors": ["The destination location already contains a different product."]
    }


@pytest.mark.django_db
def test_move_stock_invalid_quantity(client, create_stock_data):
    product, from_location, to_location, _, _ = create_stock_data
    url = reverse("move_stock")
    data = {
        "product_id": product.id,
        "from_location_id": from_location.id,
        "to_location_id": to_location.id,
        "quantity": -10,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert {"errors": ["Ensure this value is greater than or equal to 1."]}
