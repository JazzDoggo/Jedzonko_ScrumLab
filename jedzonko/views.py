from datetime import datetime

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashBoard(View):

    def get(self, request):
<<<<<<< HEAD
        return render(request, "dashboard.html")
=======
        no_of_recipes = Recipe.objects.all().count()
        no_of_plans = Plan.objects.all().count()
        return render(request, "dashboard.html", {"recipes": no_of_recipes, "plans": no_of_plans})
>>>>>>> 55ddc528ec43de8b2dd5d18b231d3af309b5c414
