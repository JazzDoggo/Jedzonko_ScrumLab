from datetime import datetime

from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe, Plan, RecipePlan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashBoard(View):
    def get(self, request):
        no_of_recipes = Recipe.objects.all().count()
        no_of_plans = Plan.objects.all().count()
        plans_by_created = Plan.objects.all().order_by('-created')
        newest_recipe_plan_meal = None
        if no_of_plans > 0:
            newest_plan = plans_by_created[0]
            newest_recipe_plan = RecipePlan.objects.filter(plan=newest_plan)
            newest_recipe_plan_days = newest_recipe_plan.day_name.all()
            newest_recipe_plan_recipes = newest_recipe_plan.recipes.all()
            newest_recipe_plan_meal = newest_recipe_plan.meals.all()
            return render(request, "dashboard.html", {
                "recipes": no_of_recipes,
                "plans": no_of_plans,
                "newest_recipe_plan_meal": newest_recipe_plan_meal,
                "newest_recipe_plan_days": newest_recipe_plan_days,
                "newest_recipe_plan_recipes": newest_recipe_plan_recipes})
        return render(request, "dashboard.html", {
            "recipes": no_of_recipes,
            "plans": no_of_plans,
            "newest_recipe_plan_meal": newest_recipe_plan_meal
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