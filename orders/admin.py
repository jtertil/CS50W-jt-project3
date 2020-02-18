from django.contrib import admin
from django.contrib.auth.models import Group

from .models import MealSize, MealType, Meal, Ingredient


class MealAdmin(admin.ModelAdmin):
    filter_horizontal = ('available_toppings', 'available_extras')
    list_display = ('name', 'type', 'price', 'is_special')
    list_filter = ('type', 'size',)
    list_select_related = ('type', 'size')


admin.site.site_header = "Pinocchio's Pizza & Subs administration site"
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient)
admin.site.register(MealSize)
admin.site.register(MealType)
admin.site.unregister(Group)





