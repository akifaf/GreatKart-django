from django import forms

from store.models import ProductGallery, ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = ReviewRating
        fields = ['subject', 'review', 'ratings']

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = ['product', 'image']