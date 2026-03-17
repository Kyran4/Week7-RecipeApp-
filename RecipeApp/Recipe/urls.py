from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from Recipe.views import edit_account
from django.db.models import Q


urlpatterns = [
    path("", views.home, name="home"),
    path("breakfast/", views.breakfast, name="breakfast"),
    path("lunch/", views.lunch, name="lunch"),
    path("dinner/", views.dinner, name="dinner"),
    path("dessert/", views.dessert, name="dessert"),
    path("drinks/", views.drinks, name="drinks"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("signup/", views.signup, name="signup"),
    path("submit_recipe/", views.submit_recipe, name="submit_recipe"),
    path("registration/login/", views.custom_login, name="login"),
    path("registration/logged_out/", views.logged_out, name="logged_out"),
    path(
        'registration/password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            success_url='/'
        ),
        name='password_change'
    ),

    path(
        'accounts/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path("registration/edit_account/", edit_account, name="edit_account"),
    path("holidays/mothers-day/", views.mothers_day, name="mothers_day"),
    path("holidays/new-year/", views.new_year, name="new_year"),

    path("health-diet/keto/", views.keto, name="keto"),
    path("health-diet/vegetarian/", views.vegetarian, name="vegetarian"),
    path("search/", views.search, name="search"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/recipes/", views.admin_recipes, name="admin_recipes"),
    path("recipe/<int:pk>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:pk>/delete/", views.delete_recipe, name="delete_recipe"),
]