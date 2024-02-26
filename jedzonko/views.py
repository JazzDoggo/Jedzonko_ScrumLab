from datetime import datetime

from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
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
