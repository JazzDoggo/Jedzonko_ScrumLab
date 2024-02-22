from datetime import datetime

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


class DashBoard(View):

    def get(self, request):
        no_of_recipes = Recipe.objects.all().count()
        return render(request, "dashboard.html", {"recipes": no_of_recipes})