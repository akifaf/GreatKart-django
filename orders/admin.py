from django.contrib import admin
from .models import Address, OrderAddress, Payment, Order, OrderProduct, Refund

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    # readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_number', 'order_total', 'is_ordered', 'created_at', 'status', 'coupon_discount']
    search_fields = ['order_number', 'first_name']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderAddress)
admin.site.register(OrderProduct)
admin.site.register(Refund)