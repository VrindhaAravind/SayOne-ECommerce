from django.urls import path
from django.shortcuts import render, redirect
from . import views
from .views import register, LoginView, seller_logout, add_product, product_list
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register', register, name='seller_registration'),
    # path('home',login_required(lambda request : render(request,'seller_base.html'),login_url='seller_login'),name='base'),
    path('home', login_required(lambda request: render(request, 'seller_home.html'), login_url='seller_login'),
         name='base'),
    path('login', LoginView, name='seller_login'),
    path('user/logout', login_required(seller_logout, login_url='seller_login'), name='seller_logout'),
    path('myprofile', login_required(views.ViewProfile, login_url='seller_login'), name='seller_profile'),
    path('editprofile', login_required(views.EditProfile.as_view(), login_url='seller_login'), name='edit_profile'),
    path('brand/add', login_required(views.create_brand, login_url='seller_login'), name='add_brand'),
    path('brand/list', login_required(views.brand_list, login_url='seller_login'), name='brand_list'),
    path('brand/remove/<int:id>', login_required(views.delete_brand, login_url='seller_login'), name='remove'),
    path('brand/change/<int:id>', login_required(views.edit_brand, login_url='seller_login'), name='update'),
    path('product/add', login_required(add_product, login_url='seller_login'), name='add_product'),
    path('products', login_required(product_list, login_url='seller_login'), name='listallproducts'),
    path('product/change/<int:id>', login_required(views.edit_product, login_url='seller_login'), name='edit_product'),
    path('orders', login_required(views.OrderListView.as_view(), login_url='seller_login'), name='orderlist'),
    path('orders/update/<int:id>', login_required(views.OrderChangeView.as_view(), login_url='seller_login'),
         name='update_order'),
    path('orders/count', login_required(views.OrderCount.as_view(), login_url='seller_login'), name='ordercount')

]

