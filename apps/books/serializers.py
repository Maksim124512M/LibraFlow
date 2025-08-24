from .models import Book, BookRent

from rest_framework.serializers import ModelSerializer


class BookSerializer(ModelSerializer):
    '''
    Serializer for the Book model.
    '''

    class Meta:
        model = Book
        fields = '__all__'


class BookRentSerializer(ModelSerializer):
    class Meta:
        model = BookRent
        fields = '__all__'