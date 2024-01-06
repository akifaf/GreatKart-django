from carts.views import _cart_id
from .models import Cart, CartItem, Wishlist

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_item = 0
    return dict(cart_count=cart_count)

def wishlist_counter(request):
    wishlist_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                wishlist = Wishlist.objects.all().filter(user=request.user)
                wishlist_count = wishlist.count()
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)