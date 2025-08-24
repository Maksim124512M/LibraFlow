from django.contrib import admin

from .models import Book, BookRent


admin.site.register(Book)
admin.site.register(BookRent)