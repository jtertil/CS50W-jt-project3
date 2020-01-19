from django.shortcuts import render

from .models import Pizza, PizzaTopping, Sub, Pasta, Salad, DinnerPlatters


def index(request):
    available_pizzas = Pizza.objects.select_related('type', 'size').all()
    available_pizzas_types = set([p.type.name for p in available_pizzas])
    available_pizzas_sizes = set([p.size.name for p in available_pizzas])
    pizza_toppings = PizzaTopping.objects.all()

    available_subs = Sub.objects.select_related('size').all()
    available_pastas = Pasta.objects.all()
    available_salads = Salad.objects.all()
    available_dinner_platters = DinnerPlatters.objects.select_related('size').all()

    context = {
        'available_pizzas': available_pizzas,
        'available_pizzas_sizes': available_pizzas_sizes,
        'available_pizzas_types': available_pizzas_types,
        'pizza_toppings': pizza_toppings,
        'available_subs': available_subs,
        'available_pastas': available_pastas,
        'available_salads': available_salads,
        'available_dinner_platters': available_dinner_platters
    }

    return render(request, 'orders/index.html', context)

