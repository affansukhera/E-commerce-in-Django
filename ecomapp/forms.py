from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Product, Contact, ShippingAddress, Review


class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SIGNUPForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'image', 'description', 'category', 'is_active', 'is_featured', 'discount_percentage', 'warranty', 'in_stock']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Is Active'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Is Featured'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount Percentage'}),
            'warranty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Warranty'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'In Stock'}),

        }
        labels = {
            'title': 'Title',
            'price': 'Price',
            'image': 'Image',
            'description': 'Description',
            'category': 'Category',
            'is_active': 'Is Active',
            'is_featured': 'Is Featured',
            'discount_percentage': 'Discount Percentage',
            'warranty': 'Warranty',
            'in_stock': 'In Stock',
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'company_name', 'area_code', 'primary_phone', 'street_address', 'zip_code', 'business_address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'area_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area Code'}),
            'primary_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Phone'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'business_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Address'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'company_name': 'Company Name',
            'area_code': 'Area Code',
            'primary_phone': 'Primary Phone',
            'street_address': 'Street Address',
            'zip_code': 'Zip Code',
            'business_address': 'Business Address',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'message', 'rating', 'product']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
            'rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }
        labels = {
            'title': 'Title',
            'message': 'Message',
            'rating': 'Rating',
        }