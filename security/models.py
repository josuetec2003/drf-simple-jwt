from django.db import models
from django.contrib.auth.models import AbstractUser

class Permission(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class User(AbstractUser):
	permission = models.ManyToManyField(Permission, blank=True)

