from rest_framework import generics

from .serializers import RegistrationSerializer
from .models import User


class RegistrationView(generics.CreateAPIView):
    '''
    View to register a new user.
    '''

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer