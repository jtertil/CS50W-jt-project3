from django.contrib import admin

from .models import MealSize, MealType, Meal, Ingredient


class MealAdmin(admin.ModelAdmin):
    filter_horizontal = ('available_ingredients',)


admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient)
admin.site.register(MealSize)
admin.site.register(MealType)





