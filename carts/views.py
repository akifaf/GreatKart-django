from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from orders.models import Address
from .models import Cart, CartItem
from store.models import Coupon, Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    # if the user is authenticated
    if current_user.is_authenticated:
        if request.method == "POST":
                cart, _ = Cart.objects.get_or_create(user=request.user)
                color = request.POST['color']
                size = request.POST['size']
                try:
                    variation = Variation.objects.get(product=product, color__color__iexact=color, size__size__iexact=size)
                    existing_cart_item = CartItem.objects.filter(product=product, variations=variation, cart=cart, user=current_user).first()

                    if existing_cart_item:
                        # If the cart item with the same variation already exists, increment quantity
                        existing_cart_item.quantity += 1
                        existing_cart_item.save()
                    else:
                        # Create a new cart item with the specified variation
                        cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user, cart=cart, variations=variation)
                        cart_item.save()
                except:
                    pass
        return redirect('cart')
    
    # if the user is not authenticated
    else:
        if request.method == "POST":
            color = request.POST.get('color')
            size = request.POST.get('size')

            try:
                variation = Variation.objects.get(product=product, color__color__iexact=color, size__size__iexact=size)
            except Variation.DoesNotExist:
                pass

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.save()

            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart, variations=variation).exists()

            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, cart=cart, variations=variation)
                cart_item.quantity += 1
                cart_item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart, variations=variation)
                item.save()

            return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            cart_obj, created = Cart.objects.get_or_create(user=request.user)
            if request.method == "POST":
                coupon_code = request.POST.get('coupon')
                if coupon_code:
                    try:
                        coupon_obj = Coupon.objects.get(coupon_code__iexact=coupon_code)
                    except Coupon.DoesNotExist:
                        messages.warning(request, "Invalid Coupon")
                        return redirect('cart') 

                    if cart_obj.coupon:
                        messages.error(request, "Coupon already applied")
                        return redirect('cart') 

                    grand_total, total, quantity, tax = cart_obj.calculate_grand_total()

                    if grand_total < coupon_obj.minimum_amount:
                        messages.warning(request, f"Minimum amount should be {coupon_obj.minimum_amount}")
                        return redirect('cart') 
                    
                    if coupon_obj.is_expired == True:
                        messages.warning(request, "Coupon has been expired!")
                        return redirect('cart') 

                    cart_obj.coupon = coupon_obj
                    cart_obj.save()
                    messages.success(request, 'Coupon applied')

            grand_total, total, quantity, tax = cart_obj.calculate_grand_total()
        else:
            cart_obj = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)               
            grand_total, total, quantity, tax = cart_obj.calculate_grand_total()

        context = {
            'cart': cart_obj,
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'store/cart.html', context)
    except ObjectDoesNotExist:
        return render(request, 'store/cart.html')


def remove_coupon(request, id):
    cart = Cart.objects.get(pk=id)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon removed")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            is_address_exists = Address.objects.filter(user=request.user).exists()            
            request.session['referrer'] = 'checkout'
            if is_address_exists:
                address = Address.objects.filter(user=request.user)
            else:
                return redirect('/orders/shipping_address?next=/carts/checkout')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'address':address
    }
    return render(request, 'store/checkout.html', context)

