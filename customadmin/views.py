from decimal import Decimal
import json
import os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import  render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Sum, Count
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear, ExtractDay

from accounts.models import Account
from orders import models
from orders.models import Order, OrderProduct, Refund
from store.forms import ImageForm
from store.models import Product, ProductGallery
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
    orders = Order.objects.filter(status='Delivered')
    total_order = orders.count()
    revenue = orders.aggregate(total_revenue=Sum('order_total'))['total_revenue']
    labels = []
    data = []
    sales = (
        Order.objects.filter(status='Delivered')
        .annotate(day=ExtractDay('created_at'))
        .values('day')
        .annotate(total_orders=Count('order_total'))
        .annotate(total_sales=Sum('order_total'))
        .order_by('day')
    )
    for i in sales:
        labels.append(f'Day {i["day"]}')
        data.append(i["total_orders"])
    print(labels, data)
    context = {
        'total_user':total_user,
        'users':users,
        'total_order':total_order,
        'revenue':revenue,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
    }
    return render(request, 'admin/admin_dashboard.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def sales_report(request):
    if request.method == 'POST':
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        type = request.POST.get('type')
        orders = Order.objects.filter(status='Delivered', created_at__gte=from_date, created_at__lte=to_date)
        labels = []
        data = []
        if type == 'weekly':
            sales = (
            Order.objects.filter(created_at__gte=from_date, created_at__lte=to_date)
            .annotate(week_number=ExtractWeek('created_at'))
            .values('week_number')
            .annotate(total_orders=Count('order_total'))
            .annotate(total_sales=Sum('order_total'))
            .order_by('week_number')
            )
            for i in sales:
                labels.append(f'Week {i["week_number"]}')
                data.append(i["total_orders"])
            print(labels, data)
        elif type == 'monthly':
            sales = (
            Order.objects.filter(created_at__gte=from_date, created_at__lte=to_date)
            .annotate(month_number=ExtractMonth('created_at'))
            .values('month_number')
            .annotate(total_orders=Count('order_total'))
            .annotate(total_sales=Sum('order_total'))
            .order_by('month_number')
            )
            for i in sales:
                labels.append(f'Month {i["month_number"]}')
                data.append(i["total_orders"])
            print(labels, data)
        else:
            sales = (
            Order.objects.filter(created_at__gte=from_date, created_at__lte=to_date)
            .annotate(year=ExtractYear('created_at'))
            .values('year')
            .annotate(total_orders=Count('order_total'))
            .annotate(total_sales=Sum('order_total'))
            .order_by('year')
            )
            for i in sales:
                labels.append(f'Year {i["year"]}')
                data.append(i["total_orders"])
            print(labels, data)
        # print(sales)
        context = {
            'orders':orders,
            'sales':sales,
            'type':type,
            'labels_json': json.dumps(labels),
            'data_json': json.dumps(data),
        }
        return render(request, 'admin/sales_report.html', context)
    return render(request, 'admin/sales_report.html')


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
    context = {
        'products':products,
    }
    return render(request,'admin/product.html', context)

def prod_gallery(request):
    products = Product.objects.all()
    product_gallery = ProductGallery.objects.all()
    print(product_gallery)
    context = {
        'products':products,
        'product_gallery':product_gallery
    }
    return render(request, 'admin/product_gallery.html', context)

def add_prod_gallery(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'message':'works'})
    else:
        print('not value')
    context = {
        'form':form
    }
    return render(request, 'admin/add_prod_gallery.html', context)

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
    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    product_form = ProductForm(instance=product)
    categories = Category.objects.all()
    print(product_gallery, 'prod_gall')
    print(product.image)
    for i in product_gallery:
        print(i.image)
    context = {
        'product':product,
        'product_form':product_form,
        'product_gallery':product_gallery,
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
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    request_refunds = Order.objects.filter(refund_requested=True, refund_granted=False)
    print(request_refunds)
    context = {
        'orders':orders,
        'request_refunds':request_refunds,
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
        subtotal += i.product.price * i.quantity
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


@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def view_return_order(request, order_id):
    orders = Order.objects.get(order_number=order_id)
    order_product = OrderProduct.objects.filter(order__order_number=order_id)
    refund = Refund.objects.get(order=orders)
    subtotal = 0
    for i in order_product:
        subtotal += i.product.price * i.quantity
    context = {
        'orders':orders,
        'order_product':order_product,
        'subtotal':subtotal,
        'refund':refund,
    }
    return render(request, 'admin/view_return_order.html', context)

@user_passes_test(user_is_admin, login_url='/customadmin/admin_login')
@login_required(login_url='/customadmin/admin_login')
@never_cache
def admin_grant_return_request(request, order_id):
    order = Order.objects.get(order_number=order_id)
    user = Account.objects.get(id=order.user.id)
    if order.refund_requested == True and order.refund_granted == False:
        order.refund_granted = True
        order.status = 'refunded'
        wallet = Decimal(str(order.order_total)) 
        user.wallet += wallet
        user.save()
        order.save()
    return redirect('order_management')
    




