from django.shortcuts import render

from .models import Pizza


def index(request):
    available_pizzas = Pizza.objects.all()
    available_pizzas_types = set([p.type.name for p in available_pizzas])
    available_pizzas_sizes = set([p.size.name for p in available_pizzas])

    context = {
        'available_pizzas': available_pizzas.order_by('type', 'size'),
        'available_pizzas_sizes': available_pizzas_sizes,
        'available_pizzas_types': available_pizzas_types
    }

    return render(request, 'orders/index.html', context)
