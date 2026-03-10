from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("health-diet/", views.health_diet, name="health_diet"),
    path("holidays/", views.holidays, name="holidays"),

    path("breakfast/", views.breakfast, name="breakfast"),
    path("lunch/", views.lunch, name="lunch"),
    path("dinner/", views.dinner, name="dinner"),

    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("accounts/signup/", views.signup, name="signup"),
    path("submit_recipe/", views.submit_recipe, name="submit_recipe"),
]