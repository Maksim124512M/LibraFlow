from rest_framework.response import Response

from ..models import BookRating, Book
from ..serializers import BookRatingSerializer



class BooksRatingServices:
    '''
    Service class for handling book rating operations such as liking and disliking books.
    '''

    @staticmethod
    def like_book(book_uuid, user) -> Response:
        '''
        Method to like a book. If the user has already liked the book, it returns a message indicating so.
        :param book_uuid:
        :param user:
        :return:
        '''

        book = Book.objects.get(uuid=book_uuid)
        rating, created = BookRating.objects.get_or_create(
            book=book,
            user=user
        )

        if not created:
            return Response({'message': 'You have already liked this book'})
        else:
            serializer = BookRatingSerializer(rating)
            book.rating += 1
            book.save()

            return Response(serializer.data)

    @staticmethod
    def dislike_book(book_uuid, user) -> tuple[bool, str]:
        '''
        Method to dislike (remove like) from a book. Only the user who liked the book or an admin can remove the like.
        :param book_uuid:
        :param user:
        :return:
        '''

        user = user

        try:
            book = Book.objects.get(uuid=book_uuid)
            rating = BookRating.objects.get(book=book)

            if user.role == 'admin' or rating.user == user:
                rating.delete()
                book.rating -= 1
                book.save()
                return True, 'Disliked successfully'

        except Book.DoesNotExist:
            return False, 'Book not found'
        except BookRating.DoesNotExist:
            return False, 'Like not found'