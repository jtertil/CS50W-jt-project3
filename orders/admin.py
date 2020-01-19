from django.contrib import admin

from .models import MealSize, MealType, Meal, Ingredient

admin.site.register(Meal)
admin.site.register(Ingredient)
admin.site.register(MealSize)
admin.site.register(MealType)





