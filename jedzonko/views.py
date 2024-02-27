from datetime import datetime

from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from jedzonko.models import Recipe, Plan, RecipePlan, DayName


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashBoard(View):
    def get(self, request):
        no_of_recipes = Recipe.objects.all().count()
        no_of_plans = Plan.objects.all().count()
        newest_recipe_plan_meal = None

        if no_of_plans > 0:
            newest_plan = Plan.objects.order_by('-created').first()
            newest_recipe_plan = RecipePlan.objects.filter(plan=newest_plan)
            newest_recipe_plan_days = newest_recipe_plan.values_list('day_name', flat=True)
            newest_recipe_plan_recipes = newest_recipe_plan.values_list('recipe', flat=True)
            newest_recipe_plan_meal = newest_recipe_plan.values_list('meal_name', flat=True)
            days = DayName.objects.all()
            recipes = Recipe.objects.all()
            for recipe in recipes:
                print(recipe.name)


        return render(request, "dashboard.html", {
            "recipes": no_of_recipes,
            "plans": no_of_plans,
            "newest_plan": newest_plan,
            "newest_recipe_plan": newest_recipe_plan,
            "newest_recipe_plan_meal": newest_recipe_plan_meal,
            "newest_recipe_plan_days": newest_recipe_plan_days,
            "days": days,
            "recipes": recipes,
            "newest_recipe_plan_recipes": newest_recipe_plan_recipes
        })


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