from django.contrib import admin
from cookbook.ingredients.models import Category, Ingredient
from cookbook.ingredients.search import index_models
index_models()
admin.site.register(Category)
admin.site.register(Ingredient)