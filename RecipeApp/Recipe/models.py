from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name="recipes")
    image = models.ImageField(upload_to="recipes/")
    short_description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()

    prep_time = models.CharField(max_length=50, blank=True)
    cook_time = models.CharField(max_length=50, blank=True)
    servings = models.CharField(max_length=20, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def ingredients_list(self):
        return [line.strip() for line in self.ingredients.split("\n") if line.strip()]