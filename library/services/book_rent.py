from django.utils import timezone
from rest_framework.exceptions import ValidationError

from library.models import Book, BookRental

MAX_ACTIVE_RENTALS = 5
MAX_RENT_DAYS = 30


def rent_book(user, book: Book):
    '''
    Rent a book to a user.
    '''

    active_rentals = BookRental.objects.filter(user=user, returned_at__isnull=True).count()
    if active_rentals >= MAX_ACTIVE_RENTALS:
        raise ValidationError('Досягнуто ліміт активних оренд.')

    rental = BookRental.objects.create(
        user=user,
        book=book,
        rented_at=timezone.now(),
        returned_at=timezone.now() + timezone.timedelta(days=MAX_RENT_DAYS)
    )

    book.save()

    return rental