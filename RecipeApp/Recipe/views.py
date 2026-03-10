from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm

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

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def login(request):
    return render(request, "registration/login.html")

@login_required
def submit_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect("recipe_detail", recipe.id)
    else:
        form = RecipeForm()
    return render(request, "Recipe/submit_recipe.html", {"form": form})
