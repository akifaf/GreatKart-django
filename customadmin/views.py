import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from accounts.models import Account
from orders.models import Order, OrderProduct
from store.models import Product
from category.models import Category
from .forms import CategoryForm, OrderForm, ProductForm
from customadmin import forms
from django.contrib.auth.decorators import user_passes_test

def user_is_admin(user):
    return  user.is_staff  

@never_cache
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_obj = Account.objects.filter(email = email)
        if not user_obj.exists():
            messages.error(request, "Account doesnot exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user_obj = auth.authenticate(email=email, password=password)

        if user_obj and user_obj.is_superadmin:
            auth.login(request, user_obj)
            return redirect('admin_dashboard')
        
        messages.error(request, "Invalid Credentials")
        return render(request, 'admin/admin_login.html')

    return render(request, 'admin/admin_login.html')


@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def admin_dashboard(request):
    users = Account.objects.filter(is_superadmin=False)
    total_user =users.count()
    context = {
        'total_user':total_user,
        'users':users
    }
    return render(request, 'admin/admin_dashboard.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def admin_logout(request):
    auth.logout(request)
    messages.info(request, "You are Logged out")
    return redirect('admin_login')

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def user_management(request):    
    users = Account.objects.filter(is_superadmin=False)
    total_user =users.count()
    context = {
        'total_user':total_user,
        'users':users
    }
    return render(request, 'admin/user_management.html', context)
@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def profile(request, pk):
    try:
        profile = Account.objects.get(pk=pk)
    except Exception as e :
        raise e
    context = {
        'profile':profile
    }
    return render(request,'admin/profile.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def block_user(request, pk):
    user = Account.objects.get(pk=pk)
    user.is_active=False
    user.is_blocked=True
    user.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    # return redirect('/customadmin/user_management')
@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def unblock_user(request, pk):
    user = Account.objects.get(pk=pk)
    user.is_active=True
    user.is_blocked=False
    user.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    # return redirect('/customadmin/user_management')

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def product(request):
    products = Product.objects.all()
    print(products.values_list('product_name'))
    context = {
        'products':products,
    }
    return render(request,'admin/product.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def add_product(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    if request.method=='POST':
        product = Product()
        product.product_name = request.POST['product_name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.stock = request.POST['stock']        
        slug = request.POST['slug']
        category = request.POST['category']
        category_id = Category.objects.get(pk=category)
        product.category = category_id
        # print(category)
        # print(slug, product.slug)
        
        if len(request.FILES) != 0:
            product.image = request.FILES['image']

        if Product.objects.filter(slug=slug):
            print("Test", Product.objects.filter(slug=slug))
            messages.error(request, "Product Slug already exists")
            return redirect('/customadmin/add_product')
        else:
            product.slug = slug
            product.save()
            messages.success(request, "Product added successfully.")

    return render(request, 'admin/add_product.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    product_form = ProductForm(instance=product)
    categories = Category.objects.all()
    
    context = {
        'product_form':product_form
    }
    if request.method=='POST':
        product_name = request.POST['product_name']
        slug = request.POST['slug']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        category = request.POST['category']
        
        if len(request.FILES) != 0:
            if len(product.image)>0:
                os.remove(product.image.path)
                product.image = request.FILES['image']

        category_id = Category.objects.get(pk=category)
        product.product_name = product_name
        product.slug = slug
        product.description = description
        product.price = price
        product.stock = stock
        product.category = category_id
        product.save()
        messages.success(request, 'Changes saved successfully')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


    return render(request, 'admin/edit_product.html', context)
    
@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    print(product.product_name)
    product.deleted = True
    product.save()
    return redirect('/customadmin/product')

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def undelete_product(request, pk):
    product = Product.objects.get(pk=pk)
    print(product.product_name)
    product.deleted = False
    product.save()
    return redirect('/customadmin/product')


@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def category(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    return render(request,'admin/category.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def add_category(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    if request.method=='POST':
        category = Category()
        category.category_name = request.POST['category_name']
        category.description = request.POST['description']
        slug = request.POST['slug']

        if len(request.FILES) != 0:
            category.cat_image = request.FILES['cat_image']

        if Category.objects.filter(slug=slug):
            print('Test2', Category.objects.filter(slug=slug))
            messages.error(request, "Category Slug already exists")
            return redirect('/customadmin/add_category')
        else:
            category.slug = slug
            category.save()
            messages.success(request, "Category added successfully.")

    return render(request, 'admin/add_category.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def edit_category(request, pk):
    category = Category.objects.get(pk=pk)
    category_form = CategoryForm(instance=category)
    categories = Category.objects.all()
    
    context = {
        'category_form':category_form
    }
    if request.method=='POST':
        category_name = request.POST['category_name']
        slug = request.POST['slug']        
        description = request.POST['description']            
        category.category_name = category_name
        category.slug = slug
        category.description = description
        if len(request.FILES) != 0:
            if len(category.image)>0:
                os.remove(category.image.path)
                category.image = request.FILES['image']
        category.save()
        messages.success(request, 'Changes saved successfully')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


    return render(request, 'admin/edit_category.html', context)
    
@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.deleted = True
    category.save()
    return redirect('/customadmin/category')

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def undelete_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.deleted = False
    category.save()
    return redirect('/customadmin/category')

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def order_management(request):
    orders = Order.objects.filter(is_ordered=True)
    context = {
        'orders':orders
    }
    return render(request,'admin/order_management.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def view_order_detail(request, order_id):
    orders = Order.objects.get(order_number=order_id)
    order_product = OrderProduct.objects.filter(order__order_number=order_id)
    subtotal = 0
    for i in order_product:
        subtotal = i.product_price * i.quantity
    context = {
        'orders':orders,
        'order_product':order_product,
        'subtotal':subtotal
    }
    return render(request, 'admin/view_order_detail.html', context) 

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def change_order_status(request, order_id):
    orders = Order.objects.get(order_number=order_id)
    if request.method == "POST":        
        status = request.POST['status']
        orders.status = status
        orders.save()
        messages.success(request, "Order status has been updated")   
    else:
        order_form = OrderForm(instance=request.user)
    order_form = OrderForm(instance=orders)
    context = {
            'orders':orders,
            'order_form':order_form,
        }
       
    return render(request, 'admin/change_order_status.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def admin_cancel_order(request, order_id):
    print('I was called')
    order = Order.objects.get(order_number=order_id)
    if order.status:
        print('I was here')
        order.status = 'Cancelled'
        order.save()
        messages.success(request, "Order Cancelled Successfully.")
    return redirect('order_management')
    




