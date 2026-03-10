from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name", "category", "image", "short_description",
            "ingredients", "instructions", "prep_time",
            "cook_time", "servings", "difficulty"
        ]