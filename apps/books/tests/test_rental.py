import pytest

from rest_framework.test import APIClient

from apps.books.models import Book, BookRent
from apps.users.models import User


@pytest.fixture
def test_user(db) -> User:
    return User.objects.create_user(username='admin2', password='password123', role='admin')


@pytest.fixture
def test_book(db, test_user) -> list[Book]:

    books = [
        Book.objects.create(title='Title', author='John Doe', publisher=test_user, isbn=10),
        Book.objects.create(title='Django for begginers', author='Jane Smith', publisher=test_user, isbn=12)
    ]

    return books


@pytest.mark.django_db
def test_rent_book(test_book):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)

    url = f'/api/v1/books/rent/{test_book[0].uuid}/'
    response = client.post(url)

    assert response.status_code == 200