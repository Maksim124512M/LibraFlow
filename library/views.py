from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    API view to list all books in the library.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=200)

class AddBookView(generics.CreateAPIView):
    """
    API view to add a new book to the library.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=201)


class UpdateBookView(generics.UpdateAPIView):
    """
    API view to update an existing book in the library.
    """

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
    """
    API view to delete a book from the library.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book = self.get_object()

        if self.request.user.role == 'admin' or self.request.user.role == 'librarian':
            # Allow admin and librarian to delete the book
            self.perform_destroy(book)

        return Response(status=204)


class DetailBookView(generics.RetrieveAPIView):
    """
    API view to retrieve the details of a specific book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book)

        return Response(serializer.data, status=200)