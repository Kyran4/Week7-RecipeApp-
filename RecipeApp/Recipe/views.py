from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models import Count

# Home / Landing Page
def home(request):
    return render(request, "Recipe/home.html")



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

def dessert(request):
    recipes = Recipe.objects.filter(category="dessert")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Dessert"})

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


def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

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

def logged_out(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

@login_required
def edit_account(request):
    recipes = Recipe.objects.filter(created_by=request.user)

    return render(
        request,
        "registration/edit_account.html",
        {"recipes": recipes}
    )   

def mothers_day(request):
    recipes = Recipe.objects.filter(category="Holidays - Mother's Day")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Mother's Day"})

def new_year(request):
    recipes = Recipe.objects.filter(category="Holidays - New Year")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "New Year"})

def keto(request):
    recipes = Recipe.objects.filter(category="Health & Diet - Keto")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Keto"})

def vegetarian(request):
    recipes = Recipe.objects.filter(category="Health & Diet - Vegetarian")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Vegetarian"})

def search(request):
    query = request.GET.get("q", "")
    recipes = Recipe.objects.filter(
        Q(name__icontains=query) |
        Q(short_description__icontains=query) |
        Q(category__icontains=query)
    )
    return render(request, "Recipe/category.html", {
        "recipes": recipes,
        "title": f"Search results for '{query}'"
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("home")

    total_users = User.objects.count()
    total_recipes = Recipe.objects.count()
    recipes_by_category = Recipe.objects.values("category").annotate(count=Count("id"))

    context = {
        "total_users": total_users,
        "total_recipes": total_recipes,
        "recipes_by_category": recipes_by_category,
    }

    return render(request, "Recipe/admin_dashboard.html", context)

@login_required
def admin_recipes(request):
    if not request.user.is_staff:
        return redirect("home")

    recipes = Recipe.objects.all().order_by("name")
    return render(request, "Recipe/admin_recipes.html", {"recipes": recipes})

@login_required
def edit_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)

    # Permission check
    if not (request.user.is_staff or recipe.created_by == request.user):
        return redirect("home")

    # Choose template based on user type
    template = (
        "Recipe/admin_edit_recipe.html"
        if request.user.is_staff
        else "Recipe/user_edit_recipe.html"
    )

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, template, {"form": form, "recipe": recipe})

@login_required
def delete_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)

    if not (request.user.is_staff or recipe.created_by == request.user):
        return redirect("home")

    template = (
        "Recipe/admin_delete_recipe.html"
        if request.user.is_staff
        else "Recipe/user_delete_recipe.html"
    )

    if request.method == "POST":
        recipe.delete()
        return redirect("edit_account")

    return render(request, template, {"recipe": recipe})