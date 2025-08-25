import pytest

from apps.books.models import Book, FavoriteBook
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
def test_favorites_list(test_user, test_book):
    FavoriteBook.objects.create(user=test_user, book=test_book[0])

    client = APIClient()
    token = AccessToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = '/api/v4/books/my-favorites/'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_add_book_to_favorite(test_user, test_book):
    client = APIClient()
    token = AccessToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = f'/api/v4/books/add-book-to-favorites/'
    response = client.post(url, data={
        'book': test_book[0].uuid,
        'user': test_user.id,
    })

    assert response.status_code == 201


@pytest.mark.django_db
def test_add_book_to_favorite(test_user, test_book):
    favorite_book = FavoriteBook.objects.create(user=test_user, book=test_book[0])

    client = APIClient()
    token = AccessToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    url = f'/api/v4/books/delete-book-from-favorites/{favorite_book.uuid}/'
    response = client.delete(url)

    assert response.status_code == 204