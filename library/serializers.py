from rest_framework.serializers import ModelSerializer

from .models import Book, Review


class BookSerializer(ModelSerializer):
    '''
    Serializer for the Book model.
    '''

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['uuid', 'created_at']


class ReviewSerializer(ModelSerializer):
    '''
    Serializer for the review model
    '''

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['uuid', 'created_at']