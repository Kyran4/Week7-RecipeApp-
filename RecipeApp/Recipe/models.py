from django.db import models

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="recipes/")
    short_description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()

    prep_time = models.CharField(max_length=50, blank=True)
    cook_time = models.CharField(max_length=50, blank=True)
    servings = models.CharField(max_length=20, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, blank=True)

    def __str__(self):
        return self.name

    @property
    def ingredients_list(self):
        return [line.strip() for line in self.ingredients.split("\n") if line.strip()]