from django.contrib import admin

from .models import PizzaTopping, Size, Pizza, PizzaType, SubExtra, Sub, Pasta, \
    Salad, DinnerPlatters

admin.site.register(Pizza)
admin.site.register(PizzaType)
admin.site.register(Size)
admin.site.register(PizzaTopping)
admin.site.register(SubExtra)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatters)




