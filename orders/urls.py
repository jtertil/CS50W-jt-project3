from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user", views.user, name="user"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cookies-check", views.cookies_check, name="cookies_check"),
    path("delete-basket-item/<int:id>", views.delete_basket_item, name="delete_basket_item"),
    path('ajax/items/', views.get_item_options, name= 'ajax_items'),
    path('ajax/extras/', views.get_extras_options, name= 'ajax_extras'),
    path('place-order/', views.place_order, name= 'place_order'),
    path('my-orders/', views.my_orders, name= 'my_orders'),


]
