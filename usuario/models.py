from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    endereco = models.CharField(max_length=255)
    data_nascimento = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
           db_table = 'Usuario'