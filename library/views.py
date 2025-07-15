from django.db.models import Count
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema

from .models import Book, BookRental, Review, Like, Dislike
from .serializers import BookSerializer, ReviewSerializer
from .services.book_rent import rent_book


# -------------------- Book Views --------------------

@extend_schema(tags=['Books'])
class BookListView(generics.ListAPIView):
    '''
    Retrieve a list of all books with optional filtering.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'published_year']


@extend_schema(tags=['Books'])
class AddBookView(generics.CreateAPIView):
    '''
    Create a new book entry. Requires authentication.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Books'])
class UpdateBookView(generics.UpdateAPIView):
    '''
    Update an existing book. Only available to admin or librarian.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request: Request, *args, **kwargs) -> Response:
        book = self.get_object()
        if request.user.role not in ['admin', 'librarian']:
            raise PermissionDenied('You do not have permission to update this book.')

        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)


@extend_schema(tags=['Books'])
class DeleteBookView(generics.DestroyAPIView):
    '''
    Delete a book. Only available to admin or librarian.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request: Request, *args, **kwargs) -> Response:
        book = self.get_object()
        if request.user.role not in ['admin', 'librarian']:
            raise PermissionDenied('You do not have permission to delete this book.')

        self.perform_destroy(book)
        return Response(status=204)


@extend_schema(tags=['Books'])
class DetailBookView(generics.RetrieveAPIView):
    '''
    Retrieve detailed information about a specific book.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'


@extend_schema(tags=['Books'])
class BookRentView(APIView):
    '''
    Rent a book. Requires authentication.
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        try:
            book = Book.objects.get(uuid=uuid)
        except Book.DoesNotExist:
            raise NotFound('Book not found.')

        rental = rent_book(request.user, book)
        return Response({
            'message': 'Book rented successfully.',
            'rental_id': rental.id,
            'due_date': rental.returned_at
        })


@extend_schema(tags=['Books'])
class BookStatsView(APIView):
    '''
    Get library statistics: total books, total rentals, most rented book.
    '''

    def get(self, request: Request, *args, **kwargs) -> Response:
        total_books = Book.objects.count()
        total_rentals = BookRental.objects.count()
        most_rented_book = Book.objects.annotate(
            rental_count=Count('rentals')
        ).order_by('-rental_count').first()

        return Response({
            'total_books': total_books,
            'total_rentals': total_rentals,
            'most_rented_book': most_rented_book.title if most_rented_book else None
        })


# -------------------- Review Views --------------------

@extend_schema(tags=['Reviews'])
class ReviewListView(generics.ListAPIView):
    '''
    Retrieve all reviews.
    '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@extend_schema(tags=['Reviews'])
class AddReviewView(generics.CreateAPIView):
    '''
    Create a new review. Requires authentication.
    '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Reviews'])
class UpdateReviewView(generics.UpdateAPIView):
    '''
    Update a review. Only admin or librarian can update any review.
    '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request: Request, *args, **kwargs) -> Response:
        review = self.get_object()
        if request.user.role not in ['admin', 'librarian']:
            raise PermissionDenied('You do not have permission to update this review.')

        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)


@extend_schema(tags=['Reviews'])
class DeleteReviewView(generics.DestroyAPIView):
    '''
    Delete a review. Only the author or admin can delete it.
    '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request: Request, *args, **kwargs) -> Response:
        review = self.get_object()
        if request.user != review.author and request.user.role != 'admin':
            raise PermissionDenied('You do not have permission to delete this review.')

        self.perform_destroy(review)
        return Response('Review deleted successfully.', status=204)


@extend_schema(tags=['Reviews'])
class ReviewDetailView(generics.RetrieveAPIView):
    '''
    Retrieve detailed information about a specific review.
    '''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'


# -------------------- Like / Dislike Views --------------------

@extend_schema(tags=['Likes'])
class LikeView(APIView):
    '''
    Like a book. User can only like a book once.
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        try:
            book = Book.objects.get(uuid=uuid)
        except Book.DoesNotExist:
            raise NotFound('Book not found.')

        like, created = Like.objects.get_or_create(book=book, author=request.user)

        if not created:
            return Response('You already liked this book.', status=400)

        book.likes += 1
        book.save()
        like.save()
        return Response('Book liked successfully.')


@extend_schema(tags=['Likes'])
class DislikeView(APIView):
    '''
    Dislike a book. User can only dislike a book once.
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        try:
            book = Book.objects.get(uuid=uuid)
        except Book.DoesNotExist:
            raise NotFound('Book not found.')

        dislike, created = Dislike.objects.get_or_create(book=book, author=request.user)

        if not created:
            return Response('You already disliked this book.', status=400)

        book.dislikes += 1
        book.save()
        dislike.save()
        return Response('Book disliked successfully.')