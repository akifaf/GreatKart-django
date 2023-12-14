from django.forms import ModelForm
from orders.models import Order
from store.models import Product
from category.models import Category

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'price', 'image', 'stock', 'category']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'description', 'cat_image']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['status']

#     def __init__(self, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'payment_method', 'address', 'order_number', 'order_total', 'status']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        readonly_fields = ['user', 'payment_method', 'address', 'order_number','order_total']

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-4'})
            if field_name in readonly_fields:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['readonly'] = True
                # field.widget.attrs['class'] = 'form-control col-4'