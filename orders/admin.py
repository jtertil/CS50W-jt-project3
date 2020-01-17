from django.contrib import admin

from .models import PizzaTopping, Size, Pizza, PizzaType

admin.site.register(Pizza)
admin.site.register(PizzaType)
admin.site.register(Size)
admin.site.register(PizzaTopping)

