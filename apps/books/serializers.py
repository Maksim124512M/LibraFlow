from .models import Book, BookRent, BookReview, BookRating

from rest_framework.serializers import ModelSerializer


class BookSerializer(ModelSerializer):
    '''
    Serializer for the Book model.
    '''

    class Meta:
        model = Book
        fields = '__all__'


class BookRentSerializer(ModelSerializer):
    '''
    Serializer for the BookRent model.
    '''

    class Meta:
        model = BookRent
        fields = '__all__'


class BookReviewSerializer(ModelSerializer):
    '''
    Serializer for the BookReview model.
    '''

    class Meta:
        model = BookReview
        fields = '__all__'


class BookRatingSerializer(ModelSerializer):
    '''
    Serializer for the BookRating model.
    '''

    class Meta:
        model = BookRating
        fields = '__all__'