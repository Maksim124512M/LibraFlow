import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    role = models.CharField(max_length=20, choices=ROLES, null=True, blank=True)
    avatar = models.ImageField(upload_to='users_avatars/', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



