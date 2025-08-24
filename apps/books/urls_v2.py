from django.urls import path

from .views.books_views import (
    BooksAPIListView, BookAPIDetailView, BookAPIUpdateView, BookAPICreateView
)

from .views.books_rent import (
    RentBookAPIView, UnrentBookAPIView
)


urlpatterns = [
    path('list/', BooksAPIListView.as_view(), name='books_list'),
    path('<uuid:uuid>/', BookAPIDetailView.as_view(), name='book_detail'),
    path('<uuid:uuid>/update/', BookAPIUpdateView.as_view(), name='book_update'),
    path('create/', BookAPICreateView.as_view(), name='book_create'),
    path('rent/<uuid:book_uuid>/', RentBookAPIView.as_view(), name='book_rent'),
    path('unrent/<uuid:book_uuid>/', UnrentBookAPIView.as_view(), name='book_unrent'),
]