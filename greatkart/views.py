from django.shortcuts import render
from store.models import Product, ReviewRating
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all().filter(deleted=False, category__deleted=False).order_by('created_date')
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    reviews = None
    context = {
        'products':products,
        'reviews':reviews,
        }
    return render(request, 'home.html', context)

