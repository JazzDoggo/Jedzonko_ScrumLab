from datetime import datetime
from random import shuffle

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Page


class IndexView(View):

    def get(self, request):
        recipes = list(Recipe.objects.all())
        shuffle(recipes)
        recipes = recipes[:3]

        ctx = {"actual_date": datetime.now(),
               "recipes": recipes}
        return render(request, "index.html", ctx)


class DashBoard(View):

    def get(self, request):
        return render(request, "dashboard.html")

class RecipeView(View):
    def get(self,request):
        return render(request, 'app-recipes.html')

def contact_page(request):
    try:
        page = Page.objects.get(slug="contact")
        return render(request, 'contact.html', {'page': page})
    except Page.DoesNotExist:
        return render(request, 'index.html')