from django.contrib import admin
from django.db.models import Sum
from .models import Coupon, Product, Variation, ReviewRating, ProductGallery, Color, Size

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'deleted')
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductGalleryInline]

    def save(self, *args, **kwargs):
        total_stock = self.variation_set.aggregate(total_stock=Sum('stock'))['total_stock']
        self.stock = total_stock 
        super().save(*args, **kwargs)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size')
   
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(Coupon)
