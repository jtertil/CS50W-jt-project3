from django.shortcuts import render

from .models import Meal, MealType


def index(request):
    m = Meal.objects.select_related('type', 'size').all()
    mt = MealType.objects.values()

    return render(request, 'orders/index.html', {'m': m, 'mt': mt})
