from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..services.book_rent import BookRentServices


class RentBookAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_uuid):
        rent_create = BookRentServices.rent_book(request, book_uuid)

        return rent_create


class UnrentBookAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_uuid):
        unrent_book = BookRentServices.unrent_book(request, book_uuid)

        return unrent_book