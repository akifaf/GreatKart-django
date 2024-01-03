from django.contrib import admin
from django.db.models import Sum

from .models import Coupon, Product, Variation, ReviewRating, ProductGallery, Color, Size
import admin_thumbnails


# class ProductVariationInline(admin.TabularInline):
#     model = ProductVariation.product_variations.through
#     extra = 1

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'deleted')
    prepopulated_fields = {'slug' : ('product_name',)}
    inlines = [ProductGalleryInline]

    def save(self, *args, **kwargs):
        # Calculate the total stock of all variations for this product
        total_stock = self.variation_set.aggregate(total_stock=Sum('stock'))['total_stock']

        # Set the product's stock field to the calculated total stock
        self.stock = total_stock 

        # Call the original save method to save the changes
        super().save(*args, **kwargs)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size')
    # prepopulated_fields = {'slug' : ('product_name',)}
    # inlines = [ProductGalleryInline]
    

# class ProductVariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'display_variation_category', 'display_variation_value', 'stock')

#     def display_variation_category(self, obj):
#         return ", ".join([var.variation_category for var in obj.product_variations.all()])
#     display_variation_category.short_description = 'Variation Category'

#     def display_variation_value(self, obj):
#         return ", ".join([var.variation_value for var in obj.product_variations.all()])
#     display_variation_value.short_description = 'Variation Value'



admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
admin.site.register(Coupon)
