from django.contrib import admin
from .models import Cart, CartItem, Wishlist

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_added', 'cart_id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'is_active']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
