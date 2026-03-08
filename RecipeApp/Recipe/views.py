from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Home / Landing Page
def home(request):
    return render(request, "Recipe/home.html")

# Static category pages
def health_diet(request):
    return render(request, "Recipe/health_diet.html")

def holidays(request):
    return render(request, "Recipe/holidays.html")

# Daily Recipe categories
def breakfast(request):
    recipes = Recipe.objects.filter(category="breakfast")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Breakfast"})

def lunch(request):
    recipes = Recipe.objects.filter(category="lunch")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Lunch"})

def dinner(request):
    recipes = Recipe.objects.filter(category="dinner")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Dinner"})

# Recipe detail page
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, "Recipe/recipe_detail.html", {"recipe": recipe})