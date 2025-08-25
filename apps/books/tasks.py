from celery import shared_task

from django.utils import timezone

from .models import BookRent


@shared_task
def check_rent_status() -> None:
    '''
    Task to check and update the status of book rents.
    '''

    BookRent.objects.filter(rent_end_date__lte=timezone.now()).delete()