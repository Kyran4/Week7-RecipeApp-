from django import forms
from .models import Recipe, Category

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Recipe
        fields = [
            "name",
            "categories",
            "image",
            "short_description",
            "ingredients",
            "instructions",
            "prep_time",
            "cook_time",
            "servings",
            "difficulty",
        ]