from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm, UserLoginForm, AddToBasketForm
from .models import Item, Basket

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# @cache_page(CACHE_TTL)
def index(request):

    m = Item.objects.select_related('type', 'size').order_by(
        'type', 'size', 'base_price')

    if request.user.is_authenticated:
        form = AddToBasketForm(request.POST)
        basket = Basket.objects.filter(user = request.user)
        if request.method == 'POST':
            if form.is_valid():
                fcd = form.cleaned_data
                bp = fcd['item'].base_price
                ep = fcd['item'].extras_price
                eq = len(form.cleaned_data['extras_selected'])

                price = bp + (ep * eq) if ep and eq else bp

                basket = Basket(
                    user=request.user,
                    item=fcd['item'],
                    special_info=fcd['special_info'],
                    price=price
                )
                basket.save()
                basket.extras_selected.set(form.cleaned_data['extras_selected'])
                basket.save()

            else:
                print(form.errors)

        return render(request, 'orders/index.html', {'m': m, 'form': form, 'basket': basket})

    return render(request, 'orders/index.html', {'m': m,})


# def get_basket(request):
#     basket = Basket.objects.filter(user=request.user)
#     return basket


def get_items(request):
    type_id = request.GET.get('type_id')
    try:
        items = Item.objects.filter(type=type_id)
    except ValueError:
        return render(request, "orders/items_options.html")

    return render(
        request, "orders/items_options.html", {'items': items})


def get_extras(request):

    item_id = request.GET.get('item_id')
    item = Item.objects.filter(id = item_id).select_related('type').first()

    extras = item.extras_available.values()
    extras_name = item.type.extras_name
    extras_max_quantity = item.extras_max_quantity
    extras_price = item.extras_price
    is_special = item.is_special

    return render(
        request, "orders/extras_options.html",
        {'extras': extras,
         'extras_name': extras_name,
         'extras_max_quantity': extras_max_quantity,
         'extras_price': extras_price,
         'is_special': is_special
         })


def user(request):
    if request.user.is_authenticated:
        return HttpResponse(f'authenticated: {request.user}')
    else:
        return HttpResponse('unauthenticated')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
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


def cookies_check(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        return HttpResponse('all good, I ate all cookies')
    else:
        request.session.set_test_cookie()
        return HttpResponse('no cookies here :( refresh and check again...')
