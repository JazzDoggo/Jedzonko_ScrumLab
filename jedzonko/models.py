from django.db import models


# Create your models here.
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.TimeField()
<<<<<<< HEAD
    votes = models.IntegerField(default=0)
=======
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    id = models.AutoField(primary_key=True)
>>>>>>> 55ddc528ec43de8b2dd5d18b231d3af309b5c414
