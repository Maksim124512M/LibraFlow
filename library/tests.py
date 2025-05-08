import json

from django.test import TestCase
from rest_framework import status

from accounts.models import User


class BookAPITestCase(TestCase):
    def setUp(self):
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

    def test_book_create(self):
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

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'Test Book')


    def test_book_update(self):
        # Create a book first
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

        book_id = response.json()['uuid']

        update_data = {
            'title': 'Updated Test Book'
        }

        response = self.client.put(
            f'/library/books/{book_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Test Book')