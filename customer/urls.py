from django.urls import path
from customer import views


urlpatterns = [
    path('account/register',views.RegistrationView.as_view(), name='register'),
    path('account/login', views.SignInView.as_view(), name='cust_signin'),
    path('account/logout',views.signout,name='signout'),
    path('home',views.HomePageView.as_view(), name='customer_home'),
    path('product/search',views.search,name="search"),
    path('category/mobiles',views.mobiles,name="mobiles"),
    path('category/laptops',views.laptops,name="laptops"),
    path('category/tablets',views.tablets,name="tablets"),
    path('sort/price_low_to_high',views.price_low_to_high,name="price_low_to_high"),
    path('sort/price_high_to_low', views.price_high_to_low, name="price_high_to_low"),
    path("brandfilter/<int:id>",views.brandfilter,name="brandfilter"),
    path("user/view_profile",views.ViewDetails.as_view(), name="view_profile"),
    path("customer/edit_profile", views.EditDetails.as_view(), name="customer_edit"),
    path('viewproduct/<int:id>', views.ViewProduct.as_view(), name='viewproduct'),
    path('addtocart/<int:id>', views.add_to_cart, name='addtocart'),
    path('products/view_cart', views.MyCart.as_view(), name='mycart'),
    path('cart/removeitem/<int:pk>', views.DeleteFromCart.as_view(), name='deletecart'),
    path("vieworders", views.view_orders, name="vieworders"),
    path("removeorder/<int:id>", views.cancel_order, name="removeorder"),
    path('viewproduct/<int:id>/writereview',views.WriteReview.as_view(),name='write_review'),
    path('editreview/<int:pk>',views.EditReview.as_view(),name='editreview'),
    path('customerservice',views.CustomerServiceView.as_view(),name='customerservice'),
    path('customerservice/<int:pk>',views.ViewService.as_view(),name='viewservice'),
    path('base',views.BasePage.as_view(),name='basepage'),
    path('cart/plus/<int:pk>',views.cart_plus,name='plus'),
    path('cart/minus/<int:pk>',views.cart_minus,name='minus'),
    path("products/checkout", views.CheckoutView, name="checkout"),
    path('order/summery/<int:id>',views.summery,name='summery'),
    path("order/proceed",views.GatewayView.as_view(),name="payment-gateway"),
    path("order/payment", views.charge, name="payment"),
    path("order/cod",views.cash_on_delivery,name="cod"),
    path('deleteaddress/<int:pk>',views.DeleteAddress.as_view(),name='deleteaddress'),
    path('editaddress/int<id>',views.editaddress,name='editaddress')
]
