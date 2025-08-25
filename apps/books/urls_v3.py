from django.urls import path

from .views.books_views import (
    BooksAPIListView, BookAPIDetailView, BookAPIUpdateView, BookAPICreateView
)

from .views.books_rent import (
    RentBookAPIView, UnrentBookAPIView
)

from .views.books_reviews import (
    CreateBookReviewAPIView, BookReviewsListView,
    BookReviewUpdateView, BookReviewDeleteView,
)


urlpatterns = [
    path('list/', BooksAPIListView.as_view(), name='books_list'),
    path('<uuid:uuid>/', BookAPIDetailView.as_view(), name='book_detail'),
    path('<uuid:uuid>/update/', BookAPIUpdateView.as_view(), name='book_update'),
    path('create/', BookAPICreateView.as_view(), name='book_create'),
    path('rent/<uuid:book_uuid>/', RentBookAPIView.as_view(), name='book_rent'),
    path('unrent/<uuid:book_uuid>/', UnrentBookAPIView.as_view(), name='book_unrent'),
    path('review/create/', CreateBookReviewAPIView.as_view(), name='create_book_review'),
    path('reviews/list/<uuid:book_uuid>/', BookReviewsListView.as_view(), name='reviews_list'),
    path('review/update/<uuid:uuid>/', BookReviewUpdateView.as_view(), name='review_update'),
    path('review/delete/<uuid:uuid>/', BookReviewDeleteView.as_view(), name='review_update'),
]