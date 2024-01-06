from django.forms import ModelForm
from django import forms
from orders.models import Order
from store.models import Color, Coupon, Product, Size, Variation
from category.models import Category

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'price', 'image', 'stock', 'category']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = ['color', 'color_code']

    def __init__(self, *args, **kwargs):
        super(ColorForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = ['size']

    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class VariationForm(ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'color', 'size', 'stock', 'image']

    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProductGalleryForm(ModelForm):
    pass

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'description', 'cat_image']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'payment_method', 'address', 'order_number', 'order_total', 'status']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        readonly_fields = ['user', 'payment_method', 'address', 'order_number','order_total']

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-8'})
            # if field_name in readonly_fields:
            #     field.widget.attrs['class'] = 'form-control'
            #     field.widget.attrs['readonly'] = True
                # field.widget.attrs['class'] = 'form-control col-4'


# class CouponForm(ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['coupon_code', 'is_expired', 'discount', 'minimum_amount']

#     def __init__(self, *args, **kwargs):
#         super(CouponForm, self).__init__(*args, **kwargs)

#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})

#         # Ensure 'is_expired' is rendered as a checkbox
#         self.fields['is_expired'].widget = forms.CheckboxInput()

