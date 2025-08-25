from django.urls import path

from .views.books_views import (
    BooksAPIListView, BookAPIDetailView, BookAPIUpdateView,
    BookAPICreateView, BookAPIReadView
)

from .views.books_rent import (
    RentBookAPIView, UnrentBookAPIView
)

from .views.books_reviews import (
    CreateBookReviewAPIView, BookReviewsListView,
    BookReviewUpdateView, BookReviewDeleteView,
)

from .views.books_rating import (
    LikeBookView, DislikeBookView
)

from .views.books_favorites import (
    FavoriteBookListView, AddBookToFavorites,
    DeleteBookFromFavorites,
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
    path('<uuid:book_uuid>/like/', LikeBookView.as_view(), name='book_like'),
    path('<uuid:book_uuid>/dislike/', DislikeBookView.as_view(), name='book_dislike'),
    path('read/<uuid:book_uuid>/', BookAPIReadView.as_view(), name='book_dislike'),
    path('my-favorites/', FavoriteBookListView.as_view(), name='books_favorites'),
    path('add-book-to-favorites/', AddBookToFavorites.as_view(), name='add_book_to_favorites'),
    path('delete-book-from-favorites/<uuid:uuid>/', DeleteBookFromFavorites.as_view(), name='delete_book_from_favorites'),
]