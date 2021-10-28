from django.urls import path
from django.shortcuts import render, redirect
from .views import register, LoginView, seller_logout, add_product
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register', register, name='seller_registration'),
    path('home', login_required(lambda request: render(request, 'seller_base.html'), login_url='seller_login'),
         name='base'),
    path('login', LoginView.as_view(), name='seller_login'),
    path('user/logout', login_required(seller_logout, login_url='seller_login'), name='seller_logout'),
    path('product/add', add_product, name='add_product')

]