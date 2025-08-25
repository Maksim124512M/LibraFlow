from .models import Book, BookRent, BookReview

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


class BookReviewSerializer(ModelSerializer):
    class Meta:
        model = BookReview
        fields = '__all__'