from datetime import datetime
from random import shuffle

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe
from django.contrib import messages
from django.urls import reverse

from jedzonko.models import Recipe, Plan, RecipePlan, DayName


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
        newest_recipe_plan_meal = None

        if no_of_plans > 0:
            newest_plan = Plan.objects.order_by('-created').first()
            newest_recipe_plan = RecipePlan.objects.filter(plan=newest_plan)
            newest_recipe_plan_days = set(newest_recipe_plan.values_list('day_name', flat=True))
            newest_recipe_plan_recipes = newest_recipe_plan.values_list('recipe', flat=True)
            newest_recipe_plan_meal = newest_recipe_plan.values_list('meal_name', flat=True)
            days = DayName.objects.all()
            recipeplans = RecipePlan.objects.all()
            recipes = Recipe.objects.all()
            days_list = []
            for day in days:
                if day.id in newest_recipe_plan_days:
                    days_list.append(day)
            recipes_list = []
            for recipe in recipes:
                if recipe.id in newest_recipe_plan_recipes:
                    recipes_list.append(recipe)

            recipeplan_list = []
            for recipeplan in recipeplans:
                for meal in newest_recipe_plan_meal:
                    if recipeplan.meal_name == meal:
                        recipeplan_list.append(recipeplan)

            for recipeplan in recipeplan_list:
                print(recipeplan.recipe.name)

        return render(request, "dashboard.html", {
            "recipes": no_of_recipes,
            "plans": no_of_plans,
            "newest_plan": newest_plan,
            "newest_recipe_plan_days": newest_recipe_plan_days,
            "recipes": recipes,
            "days_list": days_list,
            "recipeplan_list": recipeplan_list
        })


class RecipesView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipes, 50)  # LICZBA WYSWIETLANYCH KOMENTARZY NA STRONE
        page_number = request.GET.get('page')
        recipes_in_pages = paginator.get_page(page_number)
        return render(request, "app-recipes.html", {"recipes": recipes_in_pages})


class RecipeDetailView(View):
    def get(self, request, id):
        recipe_with_id = Recipe.objects.get(id=id)
        ingredient_list = recipe_with_id.ingredients.split(' ')

        return render(request, 'app-recipe-details.html',
                      {'recipe_with_id': recipe_with_id, 'ingredient_list': ingredient_list})

    def post(self, request, id):  # DODAWANIE LIKE/POST METHOD
        recipe_with_id = Recipe.objects.get(id=id)
        recipe_with_id.votes += 1
        recipe_with_id.save()
        return redirect(reverse('recipe-id', kwargs={'id': id}))


class PlanDetailView(View):
    def get(self, request, id):
        plan_with_id = Plan.objects.get(id=id)

        # SLOWNIK DO SEGREGOWANIA PRZEPISOW PO DNIACH
        recipe_plans = plan_with_id.recipeplan_set.all().order_by('order')
        grouped_day_plan = {}
        for plan in recipe_plans:
            day_name = plan.day_name
            if day_name not in grouped_day_plan:
                grouped_day_plan[day_name] = []
            grouped_day_plan[day_name].append(plan)
        return render(request, 'app-details-schedules.html',
                      {"plan_with_id": plan_with_id, "grouped_day_plan": grouped_day_plan})


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


class PlanListView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        paginator = Paginator(plans, 50)

        page_number = request.GET.get('page')
        plans_paged = paginator.get_page(page_number)
        response = render(request, 'app-schedules.html', {'plans': plans_paged})
        return response


class PlanAdd(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("plan_name")
        description = request.POST.get("plan_description")
        if name and description:
            new_plan = Plan.objects.create(name=name, description=description)
            return redirect(f"/plan/{new_plan.id}/")
        else:
            messages.add_message(request, messages.INFO, "Wypełnij poprawnie wszystkie pola")
            return redirect("/plan/add/")


class PlanAddRecipeView(View):
    def get(self, request):
        days = DayName.objects.all()
        all_plans = Plan.objects.all()
        recipes = Recipe.objects.all()

        return render(request, 'app-schedules-meal-recipe.html', {'all_plans': all_plans,
                                                                  'days': days, 'recipes': recipes,
                                                                  })

    def post(self, request):
        return redirect("/plan/add-recipe/")
