import json

from django.test import TestCase

from rest_framework import status

from .models import Book, Like, Dislike

from accounts.models import User


class BookAPITestCase(TestCase):
    def setUp(self):
        # Creating the user

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            role='admin',
        )

        response = self.client.post(
            '/accounts/api/token/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword123',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.json()['access']

        # Creating the book
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'published_year': 2023,
            'isbn': '1234567890123',
            'genre': 'fiction',
        }

        response = self.client.post(
            '/library/books/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.book_id = response.json()['uuid']

    def test_book_create(self):
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'published_year': 2023,
            'isbn': '1234567890823',
            'genre': 'fiction',
        }

        response = self.client.post(
            '/library/books/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'Test Book')


    def test_book_update(self):
        update_data = {
            'title': 'Updated Test Book'
        }

        response = self.client.put(
            f'/library/books/{self.book_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Test Book')

    def test_book_delete(self):
        response = self.client.delete(
            f'/library/books/{self.book_id}/delete/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_detail(self):
        response = self.client.get(
            f'/library/books/{self.book_id}/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Book')

    def test_book_list(self):
        response = self.client.get(
            '/library/books/?genre=fiction&published_year=2023',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_book_rent(self):
        response = self.client.post(
            f'/library/books/{self.book_id}/rent/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_book_stats(self):
        response = self.client.get(
            f'/library/books/stats/',
        )

        self.assertEqual(response.status_code, 200)


class ReviewAPITestCase(TestCase):
    def setUp(self):
        # Creating the user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            role='admin',
        )

        response = self.client.post(
            '/accounts/api/token/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword123',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.json()['access']

        # Creating the book
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'published_year': 2023,
            'isbn': '1234567890123',
            'genre': 'fiction',
        }

        response = self.client.post(
            '/library/books/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.book_id = response.json()['uuid']

        # Create new review
        data = {
            'book': self.book_id,
            'author': self.user.id,
            'content': 'Great book.'
        }

        response = self.client.post(
            '/library/books/reviews/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.review_id = response.json()['uuid']

    def test_review_list(self):
        response = self.client.get(
            '/library/books/reviews/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)

    def test_review_create(self):
        data = {
            'book': self.book_id,
            'author': self.user.id,
            'content': 'Great book.'
        }

        response = self.client.post(
            '/library/books/reviews/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['content'], 'Great book.')

    def test_review_detail(self):
        response = self.client.get(
            f'/library/books/reviews/{self.review_id}/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content'], 'Great book.')

    def test_review_update(self):
        data = {
            'content': 'Changed content',
        }

        response = self.client.put(
            f'/library/books/reviews/{self.review_id}/update/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content'], 'Changed content')

    def test_review_delete(self):
        response = self.client.delete(
            f'/library/books/reviews/{self.review_id}/delete/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            f'/library/books/reviews/{self.review_id}/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 404)


class LikesAndDislikedTestCase(TestCase):
    def setUp(self):
        # Creating the user

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            role='admin',
        )

        response = self.client.post(
            '/accounts/api/token/',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword123',
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.json()['access']

        # Creating the book
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'published_year': 2023,
            'isbn': '1234567890123',
            'genre': 'fiction',
        }

        response = self.client.post(
            '/library/books/add/',
            data=json.dumps(data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.book_id = response.json()['uuid']


    def test_like_book(self):
        response = self.client.post(
            f'/library/books/{self.book_id}/like/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        book = Book.objects.get(uuid=self.book_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.likes, 1)
        self.assertEqual(Like.objects.all().count(), 1)

    def test_dislike_book(self):
        response = self.client.post(
            f'/library/books/{self.book_id}/dislike/',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        book = Book.objects.get(uuid=self.book_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.dislikes, 1)
        self.assertEqual(Dislike.objects.all().count(), 1)

