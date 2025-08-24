import uuid

from django.db import models

from ..users.models import User


class Book(models.Model):
    '''
    Model representing a book in the library system.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='books_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    count_of_pages = models.PositiveIntegerField(null=True, blank=True)
    language_iso = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookRent(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_start_date = models.DateTimeField(auto_now_add=True)
    rent_end_date = models.DateTimeField()

    class Meta:
        verbose_name = 'BookRent'
        verbose_name_plural = 'BookRents'

    def __str__(self) -> str:
        return f'Rent {self.book.title} by {self.renter.username}'


