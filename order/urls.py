from django.urls import path

from order.views import show_cart, add_to_cart, cart_change_quantity, create_order, my_orders, cart_remove

app_name = 'order'

urlpatterns = [
    path('cart/', show_cart, name='cart'),
    path('cart_add/', add_to_cart, name='add_to_cart'),
    path('cart_remove/', cart_remove, name='cart_remove'),
    path('cart_change_quantity/', cart_change_quantity, name='cart_change_quantity'),
    path('create/', create_order, name='create_order'),
    path('my_orders/', my_orders, name='my_orders'),
]
