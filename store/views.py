from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.views import _cart_id
from carts.models import CartItem, Wishlist
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, Category, ProductGallery, ReviewRating, Variation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        pass
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, deleted=False, category__deleted=False)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(deleted=False).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.count()

    context = {
        'products':paged_products,
        'product_count':product_count,
        }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        variation = Variation.objects.filter(product=single_product)
        print(variation)
        colors = Variation.objects.filter(product=single_product).values('color__id','color__color').distinct
        sizes = Variation.objects.filter(product=single_product).values('size__id', 'size__size', 'color__id').distinct
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()   
    except Exception as e:
        raise e
        
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the review
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    
    # Get the gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)


    context = {
        'variation':variation,
        'single_product':single_product,
        'colors':colors,
        'sizes':sizes,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,
        }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        product_count = products.count()
    context = {
        'products':products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.ratings = form.cleaned_data['ratings']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
         