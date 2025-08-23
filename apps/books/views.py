from rest_framework import generics
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrLibrarian


class BooksAPIListView(generics.ListAPIView):
    queryset = Book.objects.select_related('publisher').order_by('rating')
    serializer_class = BookSerializer


class BookAPIDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    lookup_field = 'uuid'


class BookAPIUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        book = self.get_object()

        if request.user != book.publisher:
            return Response({'detail': 'You do not have permission to edit this book.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class BookAPICreateView(generics.CreateAPIView):
    queryset = Book.objects.select_related('publisher').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]