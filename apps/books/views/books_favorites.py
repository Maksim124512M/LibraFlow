from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..serializers import FavoriteBookSerializer
from ..models import FavoriteBook


class FavoriteBookListView(generics.ListAPIView):
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)


class AddBookToFavorites(generics.CreateAPIView):
    queryset = FavoriteBook.objects.select_related('book', 'user').all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]


class DeleteBookFromFavorites(generics.DestroyAPIView):
    queryset = FavoriteBook.objects.select_related('book', 'user').all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'