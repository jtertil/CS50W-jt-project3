from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Meal, MealType


def index(request):
    m = Meal.objects.select_related('type', 'size').all()
    mt = MealType.objects.values()

    return render(request, 'orders/index.html', {'m': m, 'mt': mt})


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
