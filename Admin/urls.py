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
        path('allorders',OrderList,name='all_order_list'),
        path('home/', adminhome, name='adminhome'),
        path('login/', adminlogin, name='adminlogin'),
        path('seller/', seller, name='seller'),
        path('seller_verify/<int:sid>/', verify_seller, name='seller_verify'),
        path('seller/<int:sid>/products', view_seller_prod, name='view_seller_prods'),
        path('sales/', sales, name='sales'),
        path('saller/order/', sellerorder, name='sellerorder'),
        path('logout/', logout_admin, name='logouthtml')
]