from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Meal, MealType
from .forms import MealSelectForm


def index(request):
    m = Meal.objects.select_related('type', 'size').all()

    return render(request, 'orders/index.html', {'m': m})


def user(request):
    if request.user.is_authenticated:
        return HttpResponse(f'authenticated: {request.user}')
    else:
        return HttpResponse('unauthenticated')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "orders/login.html", {'form': form})
    else:
        form = AuthenticationForm
        return render(request, "orders/login.html", {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user"))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "orders/register.html", {'form': form})
    form = UserCreationForm
    return render(request, "orders/register.html", {'form': form})


def order(request):
    form = MealSelectForm
    if request.method == 'POST':
        print(request.POST['type'])
        print(request.POST['meal'])
    return render(request, "orders/order.html", {'form': form})


def load_meals(request):
    meal_type_id = request.GET.get('id_type')
    try:
        meals = Meal.objects.filter(type=meal_type_id)
    except ValueError:
        return render(request, "orders/meals_options.html")

    try:
        desc = MealType.objects.filter(id=meal_type_id).first().description
    except ValueError:
        return render(request, "orders/meals_options.html")

    return render(
        request, "orders/meals_options.html", {'meals': meals, 'desc': desc})


def load_ingredients(request):
    meal_id = request.GET.get('id_meal')
    meal = Meal.objects.filter(id=meal_id).first()
    num_of_toppings = meal.num_of_toppings
    toppings = meal.available_toppings.values()

    num_of_extras = meal.num_of_extras
    extras = meal.available_extras.values()
    extras_price = meal.extras_price

    return render(
        request, "orders/ingredients_options.html",
        {'toppings': toppings,
         'num_of_toppings': num_of_toppings,
         'toppings_range': range(1, num_of_toppings+1),
         'extras': extras,
         'num_of_extras': num_of_extras,
         'extras_range': range(1, num_of_extras+1),
         'extras_price': extras_price
         })
