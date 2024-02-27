"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from jedzonko.views import *


#### DO SPRAWDZANIA LINKOW
def empty(request, id=0):
    return HttpResponse('Empty page')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='main-page'),
    path('main/', DashBoard.as_view(), name='dashboard'),
    path('recipe/<int:id>', RecipeDetailView.as_view(), name='recipe-id'),
    path('recipe/list/', RecipesView.as_view(), name='recipe-list'),
    path('recipe/add/', AddRecipe.as_view(), name='recipe-add'),
    # path('recipe/modify/<id>/', empty, ),
    # path('plan/<id>/', empty, ),
    path('plan/list/', PlanListView.as_view(), name='plan-list'),
    path('plan/add/', empty, name='plan-add'),
    path('plan/add-recipe/', empty, name='plan-add-recipe'),

]
