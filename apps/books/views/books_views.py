import django_filters

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request

from ..models import Book
from ..serializers import BookSerializer
from ..permissions import IsAdminOrLibrarian


class BookFilter(django_filters.FilterSet):
    '''
    Filter for searching books by title and author.
    '''

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author']


class BooksAPIListView(generics.ListAPIView):
    '''
    API view to list all books with filtering capabilities.
    '''

    queryset = Book.objects.select_related('publisher').order_by('rating')
    serializer_class = BookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = BookFilter


class BookAPIDetailView(generics.RetrieveAPIView):
    '''
    API view to retrieve details of a specific book by its UUID.
    '''

    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    lookup_field = 'uuid'


class BookAPIUpdateView(generics.UpdateAPIView):
    '''
    API view to update a specific book. Only the publisher of the book can update it.
    '''

    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]
    lookup_field = 'uuid'

    def update(self, request: Request, *args, **kwargs):
        book = self.get_object()

        if request.user != book.publisher:
            return Response({'detail': 'You do not have permission to edit this book.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class BookAPICreateView(generics.CreateAPIView):
    '''
    API view to create a new book. Only users with 'admin' or 'librarian' roles can create books.
    '''

    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]