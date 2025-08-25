from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services.books_rating import BooksRatingServices


class LikeBookView(APIView):
    '''
    View to handle liking a book.
    '''

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs) -> Response:
        book_uuid = kwargs.get('book_uuid')
        user = request.user
        like = BooksRatingServices.like_book(book_uuid, user)

        return like

class DislikeBookView(APIView):
    '''
    View to handle disliking (removing like) from a book.
    '''

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs) -> Response:
        book_uuid = kwargs.get('book_uuid')
        user = request.user
        success, message = BooksRatingServices.dislike_book(book_uuid, user)

        status_code = 200 if success else 404
        return Response({'detail': message}, status=status_code)
