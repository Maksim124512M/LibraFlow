from django.utils import timezone

from datetime import timedelta

from ..models import Book, BookRent

from rest_framework.response import Response
from rest_framework import status

from ..serializers import BookRentSerializer


class BookRentServices:

    @staticmethod
    def rent_book(request, book_uuid):
        book = Book.objects.get(uuid=book_uuid)
        rent_end_date = timezone.now() + timedelta(seconds=60)

        rental, created = BookRent.objects.get_or_create(
            book=book,
            renter=request.user,
            defaults={'rent_end_date': rent_end_date},
        )

        if not created:
            return Response({'message': 'You have already rented this book'})
        else:
            serializer = BookRentSerializer(rental)

            return Response(serializer.data)

    @staticmethod
    def unrent_book(request, book_uuid):
        user = request.user

        try:
            book = Book.objects.get(uuid=book_uuid)
            rental = BookRent.objects.get(book=book)

            if user.role in ('admin', 'librarian') or rental.renter == user:
                rental.delete()
                return Response({'message': 'Your rental was deleted successfully'})
            else:
                return Response(
                    {'error': 'You do not have permission to delete this rental'},
                    status=status.HTTP_403_FORBIDDEN
                )

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except BookRent.DoesNotExist:
            return Response({'error': 'Rental not found'}, status=status.HTTP_404_NOT_FOUND)