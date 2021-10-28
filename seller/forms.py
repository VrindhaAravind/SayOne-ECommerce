from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Seller_Details, Products


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})))
    first_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'})))

    password1 = forms.CharField(max_length=20, label="Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    password2 = forms.CharField(max_length=20, label="Confirm-Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    email = forms.CharField(max_length=100,
                            widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=500,
                              widget=(forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address'})))
    bank_name = forms.CharField(max_length=50,
                                widget=(
                                    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Name'})))
    account_number = forms.CharField(max_length=50,
                                     widget=(forms.TextInput(
                                         attrs={'class': 'form-control', 'placeholder': 'Enter Account-Number'})))
    ifsc_code = forms.CharField(max_length=15,
                                widget=(
                                    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter IDSC Code'})))

    class Meta:
        model = Seller_Details
        fields = ['address', 'bank_name', 'account_number', 'ifsc_code']


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ('user',)

        category_options = [
            ('mobile', 'Mobile'),
            ('laptop', 'Laptop'),
            ('tablet', 'Tablet')
        ]

        brand_names = [
            ('apple', 'Apple'),
            ('samsung', 'Samsung'),
            ('oneplus', 'OnePlus'),
            ('redmi', 'Redmi'),
            ('oppo', 'OPPO'),
            ('lenovo', 'Lenovo')

        ]

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'from-control'}),
            'category': forms.Select(choices=category_options),
            'brand': forms.Select(choices=brand_names, attrs={'class': 'from-control'}),

            'description': forms.TextInput(attrs={'class': 'from-control'}),
            'price': forms.NumberInput(attrs={'class': 'from-control'}),
            'stock': forms.NumberInput(attrs={'class': 'from-control'}),
            'ram': forms.TextInput(attrs={'class': 'from-control'}),
            'storage': forms.TextInput(attrs={'class': 'from-control'}),
            'color': forms.TextInput(attrs={'class': 'from-control'}),
            'offer': forms.NumberInput(attrs={'class': 'from-control'})
        }
