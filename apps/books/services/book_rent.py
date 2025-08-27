import stripe

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from datetime import timedelta

from ..models import Book, BookRent

from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_API_KEY


class BookRentServices:

    @staticmethod
    def rent_book(request, book_uuid) -> Response:
        '''
        Service to handle the book rental process, including payment via Stripe.
        :param request:
        :param book_uuid:
        :return:
        '''

        try:
            book = Book.objects.get(uuid=book_uuid)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        active_rent = BookRent.objects.filter(
            book=book,
            renter=request.user,
            rent_end_date__gt=timezone.now()
        ).first()

        if active_rent:
            return Response({'message': 'You already have an active rental for this book'})

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': book.title,
                        },
                        'unit_amount': int(book.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
                client_reference_id=str(request.user.id),
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'checkout_url': checkout_session.url})

    @staticmethod
    def create_rental_after_payment(user_id, book_uuid):
        '''
        Create a BookRent instance after successful payment.
        :param user_id:
        :param book_uuid:
        :return:
        '''

        User = get_user_model()

        try:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(uuid=book_uuid)
        except (User.DoesNotExist, Book.DoesNotExist):
            return None

        rent_end_date = timezone.now() + timedelta(days=14)
        rental = BookRent.objects.create(
            book=book,
            renter=user,
            rent_end_date=rent_end_date
        )
        return rental

    @staticmethod
    def unrent_book(request, book_uuid) -> Response:
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