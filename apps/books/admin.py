from django.contrib import admin

from .models import (
    Book, BookRent,
    BookReview, BookRating
)


admin.site.register(Book)
admin.site.register(BookRent)
admin.site.register(BookReview)
admin.site.register(BookRating)