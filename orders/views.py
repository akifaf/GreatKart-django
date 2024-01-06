import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from carts.models import Cart, CartItem
from orders.forms import AddressForm, RefundForm
from orders.models import Address, Order, OrderAddress, OrderProduct, Payment, Refund
from store.models import Product, Variation

# Create your views here.

def shipping_address(request):
    current_user = request.user
    if request.method == "POST":
        print('inside post if')
        form = AddressForm(request.POST)
        if form.is_valid():
            print('inside is_valid if')
            data = Address()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.save()
            messages.success(request, "Address added successfully")
            referrer = request.session.pop('referrer', '')
            print(referrer)
            if referrer == 'checkout':
                print('tehere')
                checkout_url = reverse('checkout')
                return redirect(checkout_url)
            else:
                print('here')
                return redirect('my_address')        
        else:
                messages.error(request, 'Invalid')
            
    else:
        form = AddressForm()
    context = {
        'form':form,
    }
    return render(request, 'store/shipping_address.html', context)

@never_cache
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)

    # If the cart is empty redirect back to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')    
    grand_total, total, quantity, tax = cart.calculate_grand_total()    

    if request.method == "POST":
        data = Order()
        data.user = current_user
        address_id = request.POST['address_id']
        address = Address.objects.get(id=address_id)
        if cart.coupon is not None:
            data.coupon_discount = cart.coupon.discount
        order_address = OrderAddress.objects.create(
        full_name=address.full_name(),
        phone_number=address.phone_number,
        email=address.email,        
        full_address=address.full_address(),
        country=address.country,
        state=address.state,
        city=address.city,
        pincode=address.pincode
        )
        data.address = order_address      
        data.order_note = request.POST['order_note']
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        payment_method = request.POST['payment_method']
        data.payment_method = payment_method        
        data.save()
        
        #Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()     

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'cart':cart,
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total
        }
        return render(request, 'orders/payments.html', context)
    else:
        return redirect("checkout")

@never_cache
def cod(request, order_id):
    current_user = request.user
    order = Order.objects.get(user=current_user, is_ordered=False, id=order_id)
    order.status = 'Ordered'
    order.is_ordered = True
    order.save()
    order.is_ordered = True
    order.save()
    
    # Move the cart item into order product table
    cart_items = CartItem.objects.filter(user=current_user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.user_id = request.user.id
        orderproduct.save()
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations = product_variation
        orderproduct.save()

    # Reduce the quantity of sold products
        product_variation = Variation.objects.get(id=item.variations.id)
        print(product_variation, "form orders page")
        product_variation.stock -= item.quantity
        product_variation.save()
    
    # Clear cart
    CartItem.objects.filter(user=request.user).delete()
    Cart.objects.filter(user=request.user).delete()

    # Send order recieved email to the customer
    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    order_number = order.order_number
    redirect_url =  f"/orders/order_complete?order_number={order_number}"
    return redirect(redirect_url)

@never_cache
def payments(request):
    user = request.user,
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    # Store transacion detail inside payment model
    payment = Payment(
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    # Move the cart item into order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        # orderproduct.ordered = True
      
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations = product_variation
        orderproduct.save()

    # Reduce the quantity of sold products
        product_variation = Variation.objects.get(id=item.variations.id)
        print(product_variation, "form orders page")
        product_variation.stock -= item.quantity
        product_variation.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()
    Cart.objects.filter(user=request.user).delete()
    
    # Send order recieved email to the customer
    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)


@never_cache
def order_complete(request):
    order_number = request.GET.get('order_number')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        # if order.payment_method == "paypal":
        #     transID = request.GET.get('payment_id')
        #     payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product.price * i.quantity
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'subtotal':subtotal,
            # 'transID':payment.payment_id,
            # 'payment':payment
        }

        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExists):
        return redirect('home')
    



