from django.shortcuts import render
from store.models import Product
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all().filter(deleted=False, category__deleted=False)

    context = {
        'products':products,
        }
    return render(request, 'home.html', context)