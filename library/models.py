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
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

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


class Review(models.Model):
    '''
    Model representing a review on book.
    '''

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review on {self.book}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-updated_at']


class Like(models.Model):
    '''
    Model for storing likes on posts.

    This model represents a like given by a user on a specific post. Each like is unique
    per user and per post.

    Attributes:
    uuid (UUID): A unique identifier for the like.
    book (ForeignKey): A foreign key to the `Post` model, indicating which post was liked.
    author (ForeignKey): A foreign key to the `User` model, indicating which user liked the post.

    Meta:
    verbose_name (str): The human-readable name for the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    unique_together (tuple): Ensures that each user can only like a post once.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='liked_books')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('author', 'book')


class Dislike(models.Model):
    '''
    Model for storing dislikes on posts.

    This model represents a dislike given by a user on a specific post. Each dislike is unique
    per user and per post.

    Attributes:
    uuid (UUID): A unique identifier for the dislike.
    book (ForeignKey): A foreign key to the `Post` model, indicating which post was disliked.
    author (ForeignKey): A foreign key to the `User` model, indicating which user disliked the post.

    Meta:
    verbose_name (str): The human-readable name for the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    unique_together (tuple): Ensures that each user can only dislike a post once.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='disliked_books')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'
        unique_together = ('author', 'book')