from django.urls import path

from .views import (
    BookListView, AddBookView,
    DeleteBookView, UpdateBookView,
    DetailBookView, BookRentView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/add/', AddBookView.as_view(), name='add-book'),
    path('books/<uuid:uuid>/', DetailBookView.as_view(), name='book-detail'),
    path('books/<uuid:uuid>/update/', UpdateBookView.as_view(), name='update-book'),
    path('books/<uuid:uuid>/delete/', DeleteBookView.as_view(), name='delete-book'),
    path('books/<uuid:uuid>/rent/', BookRentView.as_view(), name='rent-book'),
]