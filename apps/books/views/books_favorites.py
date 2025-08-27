from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..serializers import FavoriteBookSerializer
from ..models import FavoriteBook


class FavoriteBookListView(generics.ListAPIView):
    '''
    View to list all favorite books of the authenticated user.
    '''

    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteBook.objects.filter(user=self.request.user)


class AddBookToFavorites(generics.CreateAPIView):
    '''
    View to add a book to the authenticated user's favorites.
    '''

    queryset = FavoriteBook.objects.select_related('book', 'user').all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]


class DeleteBookFromFavorites(generics.DestroyAPIView):
    '''
    View to remove a book from the authenticated user's favorites.
    '''

    queryset = FavoriteBook.objects.select_related('book', 'user').all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'