from django import forms
from django.core.validators import RegexValidator

from orders.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pincode']
        
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class RefundForm(forms.Form):
    order_number = forms.CharField()
    reason = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4
    }))
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(RefundForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})