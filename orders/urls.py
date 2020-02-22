from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user", views.user, name="user"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cookies-check", views.cookies_check, name="cookies_check"),
    path('ajax/items/', views.get_items, name='ajax_items'),
    path('ajax/extras/', views.get_extras, name='ajax_extras'),


]
