from django.db import models


# Create your models here.
class Menu(models.Model):
    item = models.CharField(max_length=200)
    price = models.FloatField(max_length=100)

    def __str__(self):
        return self.item
