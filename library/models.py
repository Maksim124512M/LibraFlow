import uuid

from django.db import models

from accounts.models import User


class Book(models.Model):
    '''
    Model representing a book in the library.
    '''

    GENRES = (
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('science_fiction', 'Science Fiction'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('romance', 'Romance'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']


class BookRental(models.Model):
    '''
    Model representing a book rental.
    '''

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    rented_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} rented {self.book.title}'

    class Meta:
        verbose_name = 'Book Rental'
        verbose_name_plural = 'Book Rentals'
        ordering = ['-rented_at']
