from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user", views.user, name="user"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order", views.order, name="order"),
    path('ajax/load-meals/', views.load_meals, name='ajax_load_meals'),
]
