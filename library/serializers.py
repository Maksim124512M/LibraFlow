from rest_framework.serializers import ModelSerializer

from .models import Book


class BookSerializer(ModelSerializer):
    """
    Serializer for the Book model.
    """

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['uuid', 'created_at']