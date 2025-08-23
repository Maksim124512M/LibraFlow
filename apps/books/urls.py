from django.urls import path

from .views import (
    BooksAPIListView, BookAPIDetailView, BookAPIUpdateView, BookAPICreateView
)


urlpatterns = [
    path('list/', BooksAPIListView.as_view(), name='books_list'),
    path('<uuid:uuid>/', BookAPIDetailView.as_view(), name='book_detail'),
    path('<uuid:uuid>/update/', BookAPIUpdateView.as_view(), name='book_update'),
    path('create/', BookAPICreateView.as_view(), name='book_create'),
]