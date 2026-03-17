from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.models import User

from .models import Recipe, Category
from .forms import RecipeForm


# Home / Landing Page
def home(request):
    return render(request, "Recipe/home.html")


# -----------------------------
# DAILY CATEGORIES
# -----------------------------
def breakfast(request):
    recipes = Recipe.objects.filter(categories__name__iexact="breakfast")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Breakfast"})


def lunch(request):
    recipes = Recipe.objects.filter(categories__name__iexact="lunch")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Lunch"})


def dinner(request):
    recipes = Recipe.objects.filter(categories__name__iexact="dinner")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Dinner"})


def dessert(request):
    recipes = Recipe.objects.filter(categories__name__iexact="dessert")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Dessert"})


def drinks(request):
    recipes = Recipe.objects.filter(categories__name__iexact="drinks")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Drinks"})


# -----------------------------
# RECIPE DETAIL
# -----------------------------
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, "Recipe/recipe_detail.html", {"recipe": recipe})


# -----------------------------
# AUTH
# -----------------------------
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


# -----------------------------
# SUBMIT RECIPE 
# -----------------------------
@login_required
def submit_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            form.save_m2m() 
            return redirect("recipe_detail", recipe.id)
    else:
        form = RecipeForm()

    return render(request, "Recipe/submit_recipe.html", {"form": form})


# -----------------------------
# LOGOUT
# -----------------------------
def logged_out(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


# -----------------------------
# EDIT ACCOUNT
# -----------------------------
@login_required
def edit_account(request):
    recipes = Recipe.objects.filter(created_by=request.user)
    return render(request, "registration/edit_account.html", {"recipes": recipes})


# -----------------------------
# HOLIDAY / HEALTH CATEGORIES
# -----------------------------
def mothers_day(request):
    recipes = Recipe.objects.filter(categories__name__iexact="Holidays - Mother's Day")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Mother's Day"})


def new_year(request):
    recipes = Recipe.objects.filter(categories__name__iexact="Holidays - New Year")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "New Year"})


def keto(request):
    recipes = Recipe.objects.filter(categories__name__iexact="Health & Diet - Keto")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Keto"})


def vegetarian(request):
    recipes = Recipe.objects.filter(categories__name__iexact="Health & Diet - Vegetarian")
    return render(request, "Recipe/category.html", {"recipes": recipes, "title": "Vegetarian"})


# -----------------------------
# SEARCH
# -----------------------------
def search(request):
    query = request.GET.get("q", "")

    recipes = Recipe.objects.filter(
        Q(name__icontains=query)
        | Q(short_description__icontains=query)
        | Q(categories__name__icontains=query)
    ).distinct()

    return render(
        request,
        "Recipe/category.html",
        {"recipes": recipes, "title": f"Search results for '{query}'"},
    )


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
from django.db.models import Case, When, IntegerField, Count

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("home")

    total_users = User.objects.count()
    total_recipes = Recipe.objects.count()

    custom_order = [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Dessert",
        "Drinks",
        "Holidays - Mother's Day",
        "Holidays - New Year",
        "Health & Diet - Keto",
        "Health & Diet - Vegetarian",
    ]

    recipes_by_category = Category.objects.annotate(
        count=Count("recipes", distinct=True)
    ).order_by(
        Case(
            *[
                When(name=name, then=pos)
                for pos, name in enumerate(custom_order)
            ],
            output_field=IntegerField(),
        )
    )

    context = {
        "total_users": total_users,
        "total_recipes": total_recipes,
        "recipes_by_category": recipes_by_category,
    }

    return render(request, "Recipe/admin_dashboard.html", context)


# -----------------------------
# ADMIN RECIPE LIST
# -----------------------------
@login_required
def admin_recipes(request):
    if not request.user.is_staff:
        return redirect("home")

    recipes = Recipe.objects.all().order_by("name")
    return render(request, "Recipe/admin_recipes.html", {"recipes": recipes})


# -----------------------------
# EDIT RECIPE
# -----------------------------
@login_required
def edit_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)

    if not (request.user.is_staff or recipe.created_by == request.user):
        return redirect("home")

    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

    if request.method == "POST" and form.is_valid():
        recipe = form.save(commit=False)
        recipe.save()
        form.save_m2m()
        return redirect("recipe_detail", pk=recipe.pk)

    return render(request, "Recipe/user_edit_recipe.html", {"form": form, "recipe": recipe})


# -----------------------------
# DELETE RECIPE
# -----------------------------
@login_required
def delete_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)

    if not (request.user.is_staff or recipe.created_by == request.user):
        return redirect("home")

    if request.method == "POST":
        recipe.delete()
        return redirect("admin_recipes" if request.user.is_staff else "edit_account")

    return render(request, "Recipe/user_delete_recipe.html", {"recipe": recipe})