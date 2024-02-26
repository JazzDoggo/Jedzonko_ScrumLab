from datetime import datetime
from random import shuffle

from django.shortcuts import render, HttpResponse
from django.views import View

from jedzonko.models import *




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


class AddRecipe(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe_name = request.POST.get("recipe_name")
        recipe_description = request.POST.get("recipe_description")
        preparation_time = request.POST.get("prep_time")
        method_of_prep = request.POST.get("method_of_prep")
        ingredients = request.POST.get("ingredients")






