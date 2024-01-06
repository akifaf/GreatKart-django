from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages, auth
from decimal import Decimal

from carts.views import _cart_id
from carts.models import Cart, CartItem, Wishlist
from orders.forms import AddressForm, RefundForm
from orders.models import Address, Order, OrderProduct, Refund
from store.models import Product
from .models import Account
from .forms import RegistrationForm, UserForm

import random
from django.core.mail import send_mail
import requests

# EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            request.session['email'] = email
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            send_otp(request)
            messages.success(request, 'otp is sent to your email please verify')
            return render(request, 'accounts/otp.html' , {'email':email} )
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render (request, 'accounts/register.html', context)

@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if_user = Account.objects.get(email=email)
        
        if user is not None and user.is_verified:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # getting product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    # get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    existing_variation_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in existing_variation_list:
                            index = existing_variation_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are Logged In")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/carts/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
            
        elif if_user.is_blocked == True:
            messages.error(request, 'You are blocked')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render (request, 'accounts/login.html')


def send_otp(request):
    s=""
    for x in range(0,6):
        s+=str(random.randint(1,9))
    request.session["otp"]=s
    send_mail("otp for sign up",s,'fathimaakifa35@gmail.com',[request.session['email']],fail_silently=False)
    return render(request,"accounts/otp.html")

def  otp_verification(request):
    user = Account.objects.get(email=request.session['email'])
    if  request.method=='POST':
        user = Account.objects.get(email=request.session['email'])
        otp_=request.POST.get("otp")
        if otp_ == request.session["otp"]:
            user.is_verified=True
            user.save()
            del request.session['email']
            del request.session['otp']
            messages.info(request,'"Your OTP has been verified. Please login." ')
            return redirect('login')
        else:
            messages.error(request,"otp doesn't match")
            return render(request,'accounts/otp.html')
    else:
        user.delete()
        del request.session['email']
        return redirect('login')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "You are Logged out")
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    current_user = request.user
    user = Account.objects.get(email=current_user.email)
    orders = Order.objects.order_by('created_at').filter(user_id=user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        'user':user,
        'orders_count':orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)



def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, "Account doesnot exists")
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please Reset your password")
        return redirect("resetPassword")
    else:
        messages.error(request, "This link is has been expired")
        return redirect("login")
    
def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Password does not match")
            return redirect("resetPassword")
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def my_wallet(request):
    account = Account.objects.get(email=request.user)
    context = {
        'account':account
    }
    return render(request, 'accounts/my_wallet.html', context)

@login_required(login_url='login')
def my_address(request):
    addresses = Address.objects.filter(user=request.user)
    context = {
        'addresses':addresses
    }
    return render(request, 'accounts/my_address.html', context)

def edit_address(request, id):
    address = Address.objects.get(pk=id)
    address_form = AddressForm(instance=address)     
    context = {
        'address_form':address_form,
        'address':address,
    }
    if request.method == "POST":
        address.first_name = request.POST['first_name']
        address.last_name = request.POST['last_name']
        address.email = request.POST['email']
        address.phone_number = request.POST['phone_number']
        address.address_line_1 = request.POST['address_line_1']
        address.address_line_2 = request.POST['address_line_2']
        address.state = request.POST['state']
        address.city = request.POST['city']
        address.country = request.POST['country']
        address.pincode = request.POST['pincode']
        address.save()
        messages.success(request, "Your address has been updated")
        return redirect('my_address')
    return render(request, 'accounts/edit_address.html', context)

@login_required(login_url='login')
def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('my_address')

@login_required(login_url='login')
def edit_profile(request):
    user = Account.objects.get(email=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated")        
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
    context = {
        'user_form':user_form,
        'user':user
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def wishlist(request):
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        pass
    context = {
        'wishlist':wishlist
    }
    return render(request, 'accounts/my_wishlist.html', context)

@login_required(login_url='login')
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool':False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool':True
        }
    return JsonResponse(data)

def remove_wishlist(request, pk):
    wishlist = Wishlist.objects.get(pk=pk, user=request.user)
    wishlist.delete()
    return redirect('wishlist')

@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password doesnot match')
            return redirect('change_password')            
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product.price * i.quantity
    context = {
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal
    }
    return render(request, 'accounts/order_detail.html', context)

def cancel_order(request, order_id):
    order = Order.objects.get(order_number=order_id)
    user = order.user
    if order.status:
        order.status = 'Cancelled'
        if order.payment_method != 'COD':
            wallet = Decimal(str(order.order_total)) 
            user.wallet += wallet
            user.save()
        order.save()
        messages.success(request, "Order Cancelled Successfully.")
    return redirect('my_orders')

def request_refund(request, order_id):
    form = RefundForm()
    order = Order.objects.get(order_number=order_id)
    context = {
        'form':form,
        'order':order
    }
    if request.method == "POST":
        form = RefundForm(request.POST)
        if form.is_valid():
            ref_number = form.cleaned_data['order_number']
            reason = form.cleaned_data['reason']
            email = form.cleaned_data['email']
            try:
                order = Order.objects.get(order_number=ref_number)
                order.refund_requested = True
                order.status = 'hold'
                order.save()
                refund = Refund()
                refund.order = order
                refund.reason = reason
                refund.email = email
                refund.save()
                messages.info(request, "Your request was received.")
                return redirect('my_orders')
            except:
                messages.error(request, "This order doesnot exists")
                return redirect('my_orders')
    return render(request, 'accounts/request_refund.html', context)
