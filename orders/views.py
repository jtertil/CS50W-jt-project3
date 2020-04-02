
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import UserRegistrationForm, UserLoginForm, AddToBasketForm
from .models import Item, Basket, Order

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index(request):
    menu = get_all_items()
    if request.user.is_authenticated:

        form = AddToBasketForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                fcd = form.cleaned_data
                bp = fcd['item'].base_price
                ep = fcd['item'].extras_price
                eq = len(fcd['extras_selected'])
                price = bp + (ep * eq) if ep and eq else bp
                basket = Basket(
                    user=request.user,
                    item=fcd['item'],
                    special_info=fcd['special_info'],
                    price=price
                )
                basket.save()
                basket.extras_selected.set(fcd['extras_selected'])
                basket.save()

            else:
                print(form.errors)

        return render(
            request,
            'orders/index.html',
            {'menu': menu,
             'form': form,
             'basket': get_basket_items(request)})
    else:
        return render(request, 'orders/index.html', {'menu': menu})


# TODO login only
def get_my_orders(request):
    q = Order.objects.filter(user=request.user).order_by('status', '-pk')
    if q:
        orders = {}
        for o in q:
            orders[o.id] = {}
            orders[o.id]['data'] = o.data
            orders[o.id]['status'] = o.status
            orders[o.id]['value'] = round(float(o.value), 2)
        return orders
    else:
        return None


# TODO login only
def my_orders(request):
    orders = get_my_orders(request)
    return render(request, 'orders/my_orders.html', {'orders': orders})


# TODO login only
def get_basket_items(request, return_queryset=False):
    q = Basket.objects.prefetch_related(
        'item', 'item__type', 'extras_selected').filter(user=request.user)
    if q:
        basket_items = [i.as_dict() for i in q]
        basket_value = round(sum([i['price'] for i in basket_items]), 2)
        if return_queryset:
            return {'items': basket_items,
                    'value': basket_value,
                    'queryset': q
                    }
        else:
            return {'items': basket_items,
                    'value': basket_value
                    }
    else:
        return None


# TODO login only
def place_order(request):
    basket = get_basket_items(request, return_queryset=True)
    order = {}
    value = basket['value']
    for i, e in enumerate(basket['items']):
        order[i] = {}
        order[i]['item'] = e['item']
        if e['extras_selected']:
            order[i]['extras_selected'] = e['extras_selected']
        if e['special_info']:
            order[i]['special_info'] = e['special_info']
        order[i]['price'] = e['price']

    o = Order(user=request.user, data=order, value=value)
    o.save()
    basket['queryset'].delete()

    return JsonResponse(order)


# TODO login only
def delete_basket_item(request, id):
    q = get_object_or_404(Basket, pk=id)
    if q.user == request.user:
        q.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        raise PermissionDenied


# TODO login only
def get_all_items(**kwargs):
    # TODO refactoring need - how to deal with multiple kwargs

    if kwargs:
        k, v = kwargs.popitem()  # takes only last kwargs
        if cache.get(f'{k}:{v}'):
            items = cache.get(f'{k}:{v}')
            print(f'item {k}:{v} cache query')
            return items
        else:
            items = list(
                Item.objects.select_related(
                    'type', 'size').filter(**{k: v}))
            cache.set(f'{k}:{v}', items, CACHE_TTL)
            print(f'item {k}:{v} db query')
            return items
    else:
        if cache.get('items'):
            print('items all cache query')
            return cache.get('items')
        else:
            items = list(
                Item.objects.select_related(
                    'type', 'size').all().order_by(
                    'type', 'size', 'base_price'))
            cache.set('items', items, CACHE_TTL)
            print('items all db query')
            return items


# TODO login only
def get_item_options(request):
    type_id = request.GET.get('type_id')
    try:
        items = get_all_items(type=type_id)
    except ValueError:
        return render(request, "orders/items_options.html")
    return render(
        request, "orders/items_options.html", {'items': items})


# TODO login only
def get_extras_options(request):
    item_id = request.GET.get('item_id')
    item = get_all_items(id=item_id)[0]

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


# TODO don't need this anymore
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


# TODO login only
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
