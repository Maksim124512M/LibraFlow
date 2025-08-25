import os
import magic

from .models import Book, BookRent, BookReview, BookRating

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class BookSerializer(ModelSerializer):
    '''
    Serializer for the Book model.
    '''

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        file = attrs.get('file')

        if file:
            ext = os.path.splitext(file.name)[1].lower()
            valid_extensions = ['.pdf', '.txt', '.epub']
            if ext not in valid_extensions:
                raise serializers.ValidationError({
                    'file': f'Unsupported file extension. Allowed: {', '.join(valid_extensions)}'
                })

            mime = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)
            valid_mimes = ['application/pdf', 'text/plain', 'application/epub+zip']
            if mime not in valid_mimes:
                raise serializers.ValidationError({
                    'file': f'Unsupported file type. Allowed: {', '.join(valid_mimes)}'
                })

            max_size = 50 * 1024 * 1024
            if file.size > max_size:
                raise serializers.ValidationError({
                    'file': f'File too large. Maximum size is {max_size // (1024 * 1024)} MB.'
                })

        return attrs

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