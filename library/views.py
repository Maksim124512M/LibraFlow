from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import Book, BookRental, Review, Like, Dislike
from .serializers import BookSerializer, ReviewSerializer
from .services.book_rent import rent_book


class BookListView(generics.ListAPIView):
    '''
    API view to list all books in the library.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'published_year']


class AddBookView(generics.CreateAPIView):
    '''
    API view to add a new book to the library.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class UpdateBookView(generics.UpdateAPIView):
    '''
    API view to update an existing book in the library.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if self.request.user.role == 'admin' or self.request.user.role == 'librarian':
            # Allow admin and librarian to update the book
            self.perform_update(serializer)

        return Response(serializer.data, status=200)


class DeleteBookView(generics.DestroyAPIView):
    '''
    API view to delete a book from the library.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        book = self.get_object()

        if self.request.user.role == 'admin' or self.request.user.role == 'librarian':
            # Allow admin and librarian to delete the book
            self.perform_destroy(book)

        return Response(status=204)


class DetailBookView(generics.RetrieveAPIView):
    '''
    API view to retrieve the details of a specific book.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book)

        return Response(serializer.data, status=200)


class BookRentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        '''
        Rent a book.
        '''

        book = Book.objects.get(uuid=uuid)
        rent = rent_book(request.user, book)

        return Response(
            {
                'message': 'Book rented successfully',
                'rental_id': rent.id,
                'due_date': rent.returned_at
            },
            status=200
        )


class BookStatsView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        Get statistics about the books in the library.
        '''

        total_books = Book.objects.count()
        total_rentals = BookRental.objects.count()
        most_rented_book = Book.objects.annotate(rental_count=Count('rentals')).order_by('-rental_count').first()

        return Response({
            'total_books': total_books,
            'total_rentals': total_rentals,
            'most_rented_book': most_rented_book.title if most_rented_book else None
        })


class ReviewListView(generics.ListAPIView):
    '''
    API view to getting the list of reviews
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AddReviewView(generics.CreateAPIView):
    '''
    API view to add a review to a book.
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class UpdateReviewView(generics.UpdateAPIView):
    '''
    API view to update a review.
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if self.request.user.role == 'admin' or self.request.user.role == 'librarian':
            self.perform_update(serializer)

        return Response(serializer.data, status=200)


class DeleteReviewView(generics.DestroyAPIView):
    '''
    API view to delete a review
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        review = self.get_object()

        if request.user.role == 'admin' or request.user == review.author:
            # Allow admins and author to delete the review

            self.perform_destroy(review)

        return Response('The review was deleted', status=204)


class ReviewDetailView(generics.RetrieveAPIView):
    '''
    API view to get the details of a review
    '''

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'


class LikeView(APIView):
    '''
    API view to like a book.
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        book = Book.objects.get(uuid=uuid)
        user = request.user

        like, created = Like.objects.get_or_create(
            book=book,
            author=user,
        )

        if not created:
            return Response('You already liked this book')

        book.likes += 1

        book.save()
        like.save()

        return Response('You liked the book')


class DislikeView(APIView):
    '''
    API view to dislike a book.
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        book = Book.objects.get(uuid=uuid)
        user = request.user

        dislike, created = Dislike.objects.get_or_create(
            book=book,
            author=user,
        )

        if not created:
            return Response('You already disliked this book')

        book.dislikes += 1

        book.save()
        dislike.save()

        return Response('You disliked the book')



