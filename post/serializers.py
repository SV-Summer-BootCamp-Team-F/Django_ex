from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
    url = models.URLField(max_length=200)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.username


