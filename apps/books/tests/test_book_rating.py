import pytest

from rest_framework_simplejwt.tokens import AccessToken

from apps.books.models import Book, BookRent
from apps.users.models import User


@pytest.fixture
def test_user(db) -> User:
    return User.objects.create_user(username='admin2', password='password123', role='admin')


@pytest.fixture
def test_book(db, test_user) -> list[Book]:

    books = [
        Book.objects.create(title='Title', author='John Doe', publisher=test_user, isbn=10),
        Book.objects.create(title='Django for begginers', author='Jane Smith', publisher=test_user, isbn=12, rating=1)
    ]

    return books


def test_book_like(client, test_user, test_book):
    token = AccessToken.for_user(test_user)
    url = f'/api/v3/books/{test_book[0].uuid}/like/'

    response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == 200

    test_book[0].refresh_from_db()
    assert test_book[0].rating == 1


def test_book_dislike(client, test_user, test_book):
    token = AccessToken.for_user(test_user)
    url = f'/api/v3/books/{test_book[1].uuid}/dislike/'

    response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {token}')

    assert response.status_code == 200

    test_book[1].refresh_from_db()
    assert test_book[1].rating == 0