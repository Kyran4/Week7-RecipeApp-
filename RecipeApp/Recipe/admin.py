from django.contrib import admin
from .models import Recipe, Category
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_by', 'difficulty')
    list_filter = ('categories', 'difficulty')
    search_fields = ('name', 'short_description', 'ingredients')
    filter_horizontal = ('categories',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)