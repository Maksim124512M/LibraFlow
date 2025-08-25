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
    file = models.FileField(upload_to='books/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class BookRent(models.Model):
    '''
    Model representing the rental of a book by a user.
    '''

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


class BookReview(models.Model):
    '''
    Model representing a review of a book by a user.
    '''

    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'BookReview'
        verbose_name_plural = 'BooksReviews'

    def __str__(self) -> str:
        return f'Review on {self.book.title} by {self.author.username}'


class BookRating(models.Model):
    '''
    Model representing a like (rating) of a book by a user.
    '''

    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'BookRating'
        verbose_name_plural = 'BooksRatings'
        unique_together = ('book', 'user')

    def __str__(self) -> str:
        return f'User {self.user.username} liked "{self.book.title}"'


class FavoriteBook(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')
        ordering = ['-added_at']

    def __str__(self) -> str:
        return f'{self.user.username}s favorite book - "{self.book.title}"'


