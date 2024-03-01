from django.db import models
from django.utils.text import slugify

# Create your models here.
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.TimeField()
    votes = models.IntegerField(default=0)

class Page(models.Model):
    id = models.BigAutoField(primary_key = True)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    slug = models.SlugField(unique = True, max_length= 255 , blank = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title