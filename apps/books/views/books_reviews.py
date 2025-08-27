from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..models import BookReview
from ..serializers import BookReviewSerializer


class CreateBookReviewAPIView(generics.CreateAPIView):
    '''
    View to create a new book review.
    '''

    queryset = BookReview.objects.select_related('author', 'book').all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]


class BookReviewsListView(generics.ListAPIView):
    '''
    View to list all reviews for a specific book.
    '''

    queryset = BookReview.objects.select_related('author', 'book').all()
    serializer_class = BookReviewSerializer
    lookup_field = 'book_uuid'


class BookReviewUpdateView(generics.UpdateAPIView):
    '''
    View to update an existing book review.
    '''

    queryset = BookReview.objects.select_related('author', 'book').all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        review = self.get_object()

        if request.user != review.author:
            return Response({'detail': 'You do not have permission to edit this book.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class BookReviewDeleteView(generics.DestroyAPIView):
    '''
    View to delete an existing book review.
    '''

    queryset = BookReview.objects.select_related('author', 'book').all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        review = self.get_object()

        if request.user != review.author:
            return Response(
                {'detail': 'You do not have permission to delete this review.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().delete(request, *args, **kwargs)