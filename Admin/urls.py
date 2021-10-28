from django.urls import path
# from .views import OrderList
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .views import (
                adminhome,
                adminlogin,
                seller,
                verify_seller,
                view_seller_prod,
                sales,
                sellerorder,

                logout_admin,
                OrderList
)
urlpatterns = [
        path('allorders',login_required(OrderList,login_url='adminlogin'),name='all_order_list'),
        path('home/', login_required(adminhome,login_url='adminlogin'), name='adminhome'),
        path('login/', adminlogin, name='adminlogin'),
        path('seller/', login_required(seller,login_url='adminlogin'), name='seller'),
        path('seller_verify/<int:sid>/', login_required(verify_seller,login_url='adminlogin'), name='seller_verify'),
        path('seller/<int:sid>/products', login_required(view_seller_prod,login_url='adminlogin'), name='view_seller_prods'),
        path('sales/',login_required( sales,login_url='adminlogin'), name='sales'),
        path('saller/order/',login_required( sellerorder,login_url='adminlogin'), name='sellerorder'),
        path('logout/', login_required(logout_admin,login_url='adminlogin'), name='logouthtml')
]