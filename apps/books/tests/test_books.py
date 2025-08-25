import pytest

from apps.books.models import Book
from apps.users.models import User

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


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
def test_books_list(client) -> None:
    url = '/api/v1/books/list/'
    response = client.get(url, HTTP_ACCEPT='application/json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail(test_book, test_user) -> None:
    client = APIClient()
    token = AccessToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    book = test_book[0]
    url = f'/api/v1/books/{book.uuid}/'
    response = client.get(url, HTTP_ACCEPT='application/json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_filter(client, test_book) -> None:
    url = f'/api/v1/books/list/?title=title&author=John'
    response = client.get(url)

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['title'] == 'Title'