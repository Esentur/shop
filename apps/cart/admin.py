from django.contrib import admin

from apps.cart.models import Order, Cart, CartItem

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)

