from django.urls import path

from .views import (
    BookListView, AddBookView,
    DeleteBookView, UpdateBookView,
    DetailBookView, BookRentView,
    BookStatsView, ReviewListView,
    AddReviewView, UpdateReviewView,
    DeleteReviewView, ReviewDetailView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/add/', AddBookView.as_view(), name='add-book'),
    path('books/<uuid:uuid>/', DetailBookView.as_view(), name='book-detail'),
    path('books/<uuid:uuid>/update/', UpdateBookView.as_view(), name='update-book'),
    path('books/<uuid:uuid>/delete/', DeleteBookView.as_view(), name='delete-book'),
    path('books/<uuid:uuid>/rent/', BookRentView.as_view(), name='rent-book'),
    path('books/stats/', BookStatsView.as_view(), name='books-stats'),
    path('books/reviews/', ReviewListView.as_view(), name='book-reviews'),
    path('books/reviews/add/', AddReviewView.as_view(), name='add-review'),
    path('books/reviews/<uuid:uuid>/', ReviewDetailView.as_view(), name='review-detail'),
    path('books/reviews/<uuid:uuid>/update/', UpdateReviewView.as_view(), name='update-review'),
    path('books/reviews/<uuid:uuid>/delete/', DeleteReviewView.as_view(), name='delete-review'),
]