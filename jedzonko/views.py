from datetime import datetime
from random import shuffle

from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from jedzonko.models import Recipe

from jedzonko.models import Recipe, Plan


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
        no_of_recipes = Recipe.objects.all().count()
        no_of_plans = Plan.objects.all().count()
        return render(request, "dashboard.html", {"recipes": no_of_recipes, "plans": no_of_plans})



class RecipesView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipes, 50)  ## LICZBA WYSWIETLANYCH KOMENTARZY NA STRONE
        page_number = request.GET.get('page')
        recipes_in_pages = paginator.get_page(page_number)
        return render(request, "app-recipes.html", {"recipes": recipes_in_pages})

      
class RecipeDetailView(View):
    def get(self, request, id):
        return HttpResponse('RECIPE DETAILS ' + id)