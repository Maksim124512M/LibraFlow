from django.urls import path, include


urlpatterns = [
    path('books/', include('apps.books.urls_v3')),
]