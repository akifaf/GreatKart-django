from django.forms import ModelForm
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