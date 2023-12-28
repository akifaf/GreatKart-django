from django.db import models
from accounts.models import Account
from category.models import Category
from django.urls import reverse
from django.db.models import Avg, Count

# Create your models here.   

class Banner(models.Model):
    image = models.ImageField(upload_to='photos/banner')
    alt_text = models.CharField(max_length=200)

class Size(models.Model):
    size = models.CharField(max_length=100)

    def __str__(self):
        return self.size

class Color(models.Model):
    color = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    def __str__(self):
        return self.color

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def total_stock(self):
        variations = self.productvariation_set.all()
        total_stock = sum(variation.stock for variation in variations)
        return total_stock

    def __str__(self):
        return self.product_name    
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('ratings'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.product.product_name}'






# class VaritationManager(models.Manager):
#     def colors(self):
#         return super(VaritationManager, self).filter(variation_category = 'color', is_active=True)    
    
#     def sizes(self):
#         return super(VaritationManager, self).filter(variation_category = 'size', is_active=True)    

# varitation_category_choice = (
#     ('color', 'color'),
#     ('size', 'size')
# )

# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
#     variation_category = models.CharField(max_length=100, choices=varitation_category_choice, default='color')
#     variation_value = models.CharField(max_length=100, null=True)
#     is_active = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)

#     objects = VaritationManager()

#     def __str__(self):
#         return f'{self.variation_category} : {self.variation_value} '
    
# class ProductVariation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
#     product_variations = models.ManyToManyField(Variation, blank=True)
#     stock = models.IntegerField()

#     def __str__(self):
#         return f'{self.product}'
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products/', max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'

    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    ratings = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

