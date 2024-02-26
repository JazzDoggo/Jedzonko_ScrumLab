from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashBoard(View):

    def get(self, request):
        no_of_recipes = Recipe.objects.all().count()
        return render(request, "dashboard.html", {"recipes": no_of_recipes})


class AddRecipe(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):

        name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('recipe_description')
        preparation_time = request.POST.get('preparation_time')
        instructions = request.POST.get('instructions')

        if all([name, ingredients, description, preparation_time, instructions]):
            Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                                  preparation_time=preparation_time, instructions=instructions)
            return redirect('/recipe/list/')

        else:
            messages.add_message(request, messages.INFO, "Wypełnij poprawnie wszystkie pola")
            return redirect("/recipe/add/")
