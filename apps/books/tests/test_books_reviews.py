import pytest
import json

from rest_framework_simplejwt.tokens import AccessToken

from apps.books.models import Book, BookReview
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


@pytest.fixture
def test_review(db, test_user, test_book) -> BookReview:
    return BookReview.objects.create(book=test_book[0], author=test_user, content='Very cool book')


def test_review_publish(client, test_user, test_book):
    token = AccessToken.for_user(test_user)

    url = '/api/v3/books/review/create/'
    response = client.post(
        url,
        data={
            'book': str(test_book[0].uuid),
            'author': test_user.id,
            'content': 'very cool book',
        },
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    assert response.status_code in [200, 201]
    assert response.json()['content'] == 'very cool book'


def test_reviews_list(client, test_book):
    url = f'/api/v3/books/reviews/list/{test_book[0].uuid}/'
    response = client.get(url)

    assert response.status_code == 200


def test_review_update(client, test_review, test_user):
    token = AccessToken.for_user(test_user)

    url = f'/api/v3/books/review/update/{test_review.uuid}/'
    response = client.patch(
        url,
        data=json.dumps({'content': 'updated content'}),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    assert response.status_code in [200, 201]
    assert response.json()['content'] == 'updated content'


def test_review_delete(client, test_review, test_user):
    token = AccessToken.for_user(test_user)

    url = f'/api/v3/books/review/delete/{test_review.uuid}/'
    response = client.delete(
        url,
        HTTP_AUTHORIZATION=f'Bearer {token}'
    )

    assert response.status_code == 204