from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.book_rent import BookRentServices


class RentBookAPIView(generics.CreateAPIView):
    '''
    View for renting a book.
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, book_uuid) -> Response:

        return BookRentServices.rent_book(request, book_uuid)


class UnrentBookAPIView(generics.DestroyAPIView):
    '''
    View for unrenting a book.
    '''

    permission_classes = [IsAuthenticated]

    def delete(self, request, book_uuid) -> Response:
        return BookRentServices.unrent_book(request, book_uuid)