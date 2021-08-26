from django.conf import settings
from django.db import models
from django.http.response import Http404


# Create your models here.


class RabbitHole(models.Model):
    '''
    Rabbits live in rabbit holes
    '''
    location = models.CharField(max_length=64, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bunnies_limit = models.PositiveIntegerField(default=5)


class Bunny(models.Model):
    '''
    Rabbits are mammals
    '''
    name = models.CharField(max_length=64)
    home = models.ForeignKey(RabbitHole, on_delete=models.CASCADE, related_name='bunnies')
