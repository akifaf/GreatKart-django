from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Enter password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':"Confirm password"
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Your Email"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter Your Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = str(cleaned_data.get('phone_number'))

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

        if not phone_number.isdigit() or len(phone_number) != 10 or phone_number.startswith('0'):
            raise forms.ValidationError('Invalid phone number.')
        
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'address_line_1', 'address_line_2', 'profile_picture', 'city', 'state', 'country')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'