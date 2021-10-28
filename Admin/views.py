from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import ListView
from customer.models import Orders
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, auth
from .models import Staff

from seller.models import Seller_Details, Products

from customer.models import Userdetails
from django.contrib import messages


# Create your views here.

def OrderList(request):
    all_orders = Orders.objects.all()

    return render(request, 'all_orders.html', {'all_orders': all_orders})


def adminlogin(request):
    if request.method == 'POST':
        # print(request.POST.get('username'), request.POST.get('pswd'))
        if Staff.objects.filter(username=request.POST.get('username'), password=request.POST.get('pswd')).exists():
            # print('yes')
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('pswd'))
            # print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('adminhome')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('adminlogin')

    return render(request, 'adminLogin.html')


def adminhome(request):
    pending = Seller_Details.objects.filter(status='pending')
    print(len(pending))
    orders = (Orders.objects.exclude(status='pending'))
    sellers = (Seller_Details.objects.all())
    customers = (Userdetails.objects.all())
    print('No of orders : ', orders)
    print('No of Sellers : ', sellers)
    print('No of Customers :', customers)
    sum = 0
    for i in orders:
        sum += (i.quantity * i.product.price)
    print(sum)
    return render(request, 'adminHome.html',
                  {'pending': len(pending), 'orders': len(orders), 'sellers': len(sellers), 'customers': len(customers),
                   'sales': sum})


def seller(request):
    pending = Seller_Details.objects.filter(status='pending')
    sellers = Seller_Details.objects.filter(status='approved')
    return render(request, 'adminSeller.html', {'pending': pending, 'sellers': sellers})


def verify_seller(request, *args, **kwargs):
    print(kwargs.get('sid'))
    if request.method == "POST":
        s = Seller_Details.objects.get(id=kwargs.get('sid'))
        s.status = 'approved'
        s.save()
        print('verified')
        return redirect('seller')
    seller = Seller_Details.objects.get(id=kwargs.get('sid'))
    return render(request, 'verify_seller.html', {'seller': seller})


def view_seller_prod(request, *args, **kwargs):
    dets = Seller_Details.objects.get(id=kwargs.get('sid'))
    print(kwargs.get('sid'))
    x = Seller_Details.objects.get(id=kwargs.get('sid')).user
    products = Products.objects.filter(user=x)

    print(x)
    print(products)
    return render(request, 'sellerProd.html', {'products': products, 'details': dets})


def sales(request):
    sales = Orders.objects.exclude(status='pending')
    sellers = [i[0] for i in sales.values_list('seller').distinct()]
    # print(sellers)
    status = [i[0] for i in sales.values_list('status').distinct()]
    # print(status)
    s = []
    for i in sales:
        val = {}
        val['product'] = i.product.product_name
        val['seller'] = i.seller
        val['customer'] = i.user
        val['status'] = i.status
        val['amt'] = (i.quantity * i.product.price)
        s.append(val)
    # print(s)
    if request.method == 'POST':
        # print(request.POST.get('seller'))
        # print(sales.filter(seller=request.POST.get('seller')))
        if request.POST.get('seller') == 'All':
            x = s
        else:
            x = sales.filter(seller=request.POST.get('seller'))
            seller = request.POST.get('seller')
            x = []
            for i in s:
                if i['seller'] == seller:
                    x.append(i)

        return render(request, 'salesHome.html', {'sales': x, 'sellers': sellers, 'status': status})
    return render(request, 'salesHome.html', {'sales': s, 'sellers': sellers, 'status': status})


def sellerorder(request):
    return render(request, 'salesHome.html')


def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')