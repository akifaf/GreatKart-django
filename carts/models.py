from django.db import models
from accounts.models import Account

from store.models import Coupon, Product, Variation

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    def calculate_grand_total(self):
        cart_items = CartItem.objects.filter(cart=self, is_active=True)
        total = 0
        quantity = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = tax + total
        if self.coupon is not None:
            if grand_total > self.coupon.minimum_amount:
                grand_total = round(grand_total - self.coupon.discount, 2)
        return grand_total, total, quantity, tax
    
class CartItem(models.Model): 
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price *self.quantity
    
    def __unicode__(self):
        return self.product
    
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.product_name
