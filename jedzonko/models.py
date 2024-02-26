from django.db import models


# Create your models here.
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    instructions = models.TextField()


class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    id = models.AutoField(primary_key=True)
    meal_name = models.CharField(max_length=128)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField(unique=True)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

