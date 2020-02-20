from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .forms import MealSelectForm, UserRegistrationForm, UserLoginForm
from .models import Meal, MealType

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def index(request):
    m = Meal.objects.select_related('type', 'size').order_by(
        'type', 'size', 'price')

    return render(request, 'orders/index.html', {'m': m})


def user(request):
    if request.user.is_authenticated:
        return HttpResponse(f'authenticated: {request.user}')
    else:
        return HttpResponse('unauthenticated')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request = request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "orders/login.html", {'form': form})
    else:
        form = UserLoginForm
        return render(request, "orders/login.html", {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user"))


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "orders/register.html", {'form': form})
    form = UserRegistrationForm
    return render(request, "orders/register.html", {'form': form})


def order(request):
    # request.session['cart'] = []
    form = MealSelectForm(request.POST)

    # if not form.is_valid():
    #     print(form.errors)

    if request.method == 'POST' and form.is_valid():
        add_to_cart(request, form)

    return render(request, "orders/order.html", {'form': form})


def add_to_cart(request, form):
    cart = request.session.get('cart', [])
    request.session['cart'] = cart

    fcd = form.cleaned_data
    ordered_meal = {
        'type': {
            'id': fcd['meal'].type_id,
            'name': fcd['meal'].type.name},
        'size': {
            'id': fcd['meal'].size_id,
            'name': fcd['meal'].size.name if fcd['meal'].size_id else None},
        'meal': {
            'id': fcd['meal'].id,
            'name': fcd['meal'].name},
        'toppings': [
            {'id': t.id, 'name': t.name} for t in
            fcd['toppings'][:fcd['meal'].num_of_toppings]
        ],
        'extras': [
            {'id': e.id, 'name': e.name} for e in
            fcd['extras'][:fcd['meal'].num_of_extras]
        ],
        'is_special':
            fcd['meal'].is_special,
        'special_instructions':
            fcd['special_instructions'],
        'base_price':
            float(fcd['meal'].price),
        'total_price':
            float(fcd['meal'].calculate_total_price(len(fcd['extras'])))
    }
    print(ordered_meal)
    cart.append(ordered_meal)


def get_cart(request):
    c = request.session['cart']
    c_value = round(sum(i['total_price'] for i in request.session['cart']), 2)

    return render(
        request, "orders/cart.html", {'cart': c, 'c_value': c_value})


def load_meals(request):
    meal_type_id = request.GET.get('id_type')
    try:
        meals = Meal.objects.filter(type = meal_type_id)
    except ValueError:
        return render(request, "orders/meals_options.html")

    try:
        desc = MealType.objects.filter(id = meal_type_id).first().description
    except ValueError:
        return render(request, "orders/meals_options.html")

    return render(
        request, "orders/meals_options.html", {'meals': meals, 'desc': desc})


def load_ingredients(request):
    meal_id = request.GET.get('id_meal')
    meal = Meal.objects.filter(id = meal_id).first()
    num_of_toppings = meal.num_of_toppings
    toppings = meal.available_toppings.values()

    num_of_extras = meal.num_of_extras
    extras = meal.available_extras.values()
    extras_price = meal.extras_price

    is_special = meal.is_special

    return render(
        request, "orders/ingredients_options.html",
        {'toppings': toppings,
         'num_of_toppings': num_of_toppings,
         'toppings_range': range(1, num_of_toppings + 1),
         'extras': extras,
         'num_of_extras': num_of_extras,
         'extras_range': range(1, num_of_extras + 1),
         'extras_price': extras_price,
         'is_special': is_special
         })


def cookies_check(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return HttpResponse('all good, I ate all cookies')
    else:
        request.session.set_test_cookie()
        return HttpResponse('no cookies here :( refresh and check again...')
