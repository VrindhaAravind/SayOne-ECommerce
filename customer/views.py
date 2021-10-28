from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .forms import RegistrationForm, LoginForm, UserForm, UpdateForm, ReviewForm, PlaceOrderForm, CustomerServiceForm
from .models import Cart, Review, Userdetails, Orders, Address, CustomerService
from seller.models import Products, Brand
from .decorators import signin_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import IntegerField, Case, Value, When
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
from django.db.models import Sum


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "cust_registration.html"
    success_url = reverse_lazy("cust_signin")


class SignInView(TemplateView):
    template_name = "cust_login.html"
    form_class = LoginForm
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request, "Login Successful")
                return redirect("customer_home")
            else:
                messages.error(request, 'Username or Password is incorrect')
                self.context["form"] = form
                return render(request, self.template_name, self.context)


@signin_required
def signout(request):
    logout(request)
    return redirect("cust_signin")


@method_decorator(signin_required, name="dispatch")
class HomePageView(ListView):
    template_name = 'homepage.html'
    model = Products
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = Products.objects.all()
        brands = Brand.objects.all()
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            page_products = paginator.page(page)
        except PageNotAnInteger:
            page_products = paginator.page(1)
        except EmptyPage:
            page_products = paginator.page(paginator.num_pages)

        context['products'] = page_products
        context['brands'] = brands
        return context


class BasePage(TemplateView):
    template_name = 'cust_base.html'
    context = {}

    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        print(brands)
        self.context['brands'] = brands
        return render(request, self.template_name, self.context)


def search(request):
    search = request.GET['q']
    product = Products.objects.filter(product_name__icontains=search)
    brands = Brand.objects.all()
    context = {'product': product, "brands": brands}
    return render(request, 'search.html', context)


def mobiles(request):
    mobiles = Products.objects.filter(category='mobile')
    brands = Brand.objects.all()
    context = {'mobiles': mobiles, "brands": brands}
    return render(request, 'category.html', context)


def laptops(request):
    laptops = Products.objects.filter(category="laptop")
    brands = Brand.objects.all()
    context = {'laptops': laptops, "brands": brands}
    return render(request, 'category.html', context)


def tablets(request):
    tablets = Products.objects.filter(category="tablet")
    brands = Brand.objects.all()
    context = {'tablets': tablets, "brands": brands}
    return render(request, 'category.html', context)


def price_low_to_high(request):
    low = Products.objects.all().order_by('price')
    brands = Brand.objects.all()
    context = {'low': low, "brands": brands}
    return render(request, 'category.html', context)


def price_high_to_low(request):
    high = Products.objects.all().order_by('-price')
    brands = Brand.objects.all()
    context = {'high': high, "brands": brands}
    return render(request, 'category.html', context)


def brandfilter(request, id):
    brand = Brand.objects.get(id=id)
    brands = Brand.objects.all()
    products = Products.objects.filter(brand=brand)
    context = {'products': products, "brands": brands}
    return render(request, "category.html", context)


class EditDetails(TemplateView):
    user_form = UserForm
    profile_form = UpdateForm
    template_name = "user_details.html"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None
        try:
            details = Userdetails.objects.get(user=request.user)
        except Userdetails.DoesNotExist:
            details = None
        user_form = UserForm(post_data, instance=request.user)
        profile_form = UpdateForm(post_data, file_data, instance=details)
        brands=Brand.objects.all()

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse_lazy('view_profile'))
        context = self.get_context_data(user_form=user_form, profile_form=profile_form,brands=brands)

        return self.render_to_response(context)


class ViewDetails(TemplateView):
    template_name = "my_profile.html"
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            user_details = Userdetails.objects.get(user=self.request.user)
            brands = Brand.objects.all()
            self.context["brands"] = brands
            self.context['user_details'] = user_details
            self.context['user'] = self.request.user
            return render(request, self.template_name, self.context)

        except Userdetails.DoesNotExist:
            return redirect("edit_profile")


@method_decorator(signin_required, name="dispatch")
class ViewProduct(TemplateView):
    template_name = 'productdetail.html'
    context = {}

    def get(self, request, *args, **kwargs):
        stock_exceeded = False
        id = kwargs['id']
        brands = Brand.objects.all()
        product = Products.objects.get(id=id)
        reviews = Review.objects.filter(product=product)
        my_reviews = Review.objects.filter(user=request.user, product=product)
        similar_products = Products.objects.filter(brand=product.brand, category=product.category)
        cart_products = Cart.objects.filter(user=request.user, status='ordernotplaced')
        for cart in cart_products:
            if (product == cart.product) & (product.stock == cart.quantity):
                stock_exceeded = True
                break
        self.context['product'] = product
        self.context['brands'] = brands
        self.context['reviews'] = reviews
        self.context['my_reviews'] = my_reviews
        self.context['similar_products'] = similar_products
        self.context['stock_exceeded'] = stock_exceeded
        return render(request, self.template_name, self.context)


@signin_required
def add_to_cart(request, *args, **kwargs):
    id = kwargs['id']
    product = Products.objects.get(id=id)
    if Cart.objects.filter(product=product, user=request.user, status='ordernotplaced').exists():
        cart = Cart.objects.get(product=product, user=request.user)
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart(product=product, user=request.user)
        cart.save()
        print('product added')
    return redirect('mycart')



@method_decorator(signin_required, name="dispatch")
def cart_count(user):
    cnt = Cart.objects.filter(user=user, status='ordernotplaced').count()
    return cnt


class MyCart(TemplateView):
    template_name = 'cart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        cart_products = Cart.objects.filter(user=request.user, status='ordernotplaced')
        total = 0
        brands = Brand.objects.all()
        for cart in cart_products:
            if cart.quantity > cart.product.stock:
                cart.quantity = cart.product.stock
                cart.save()
            if (cart.quantity == 0) & (cart.product.stock != 0):
                cart.quantity = 1
                cart.save()
            total += cart.product.price * cart.quantity
        # print(total)
        self.context["brands"] = brands
        self.context['cart_products'] = cart_products
        self.context['total'] = total
        # self.context['cnt']=cart_count(request.user)
        return render(request, self.template_name, self.context)


def cart_plus(request, *args, **kwargs):
    id = kwargs['pk']
    cart = Cart.objects.get(id=id)
    cart.quantity += 1
    cart.save()
    return redirect('mycart')


def cart_minus(request, *args, **kwargs):
    id = kwargs['pk']
    cart = Cart.objects.get(id=id)
    cart.quantity -= 1
    cart.save()
    if cart.quantity < 1:
        return redirect('deletecart', cart.id)
    return redirect('mycart')


@method_decorator(signin_required, name="dispatch")
class DeleteFromCart(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        cart_product = Cart.objects.get(id=id)
        cart_product.delete()
        return redirect('mycart')


class WriteReview(TemplateView):
    template_name = 'review.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        brands = Brand.objects.all()
        self.context['brands'] = brands
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        product = Products.objects.get(id=id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            new_review = Review(user=request.user, product=product, review=review)
            new_review.save()
            return redirect('viewproduct', product.id)


class EditReview(TemplateView):
    template_name = 'editreview.html'
    context = {}

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        my_review = Review.objects.get(id=id)
        instance = {
            'review': my_review.review
        }
        form = ReviewForm(initial=instance)
        brands = Brand.objects.all()
        self.context['form'] = form
        self.context['brands'] = brands
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        my_review = Review.objects.get(id=id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data.get('review')
            my_review.review = review
            my_review.save()
            return redirect('viewproduct', my_review.product.id)


class CustomerServiceView(TemplateView):
    template_name = 'customerservice.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = CustomerServiceForm()
        services = CustomerService.objects.filter(user=request.user)
        brands = Brand.objects.all()
        self.context['form'] = form
        self.context['services'] = services
        self.context['brands'] = brands
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = CustomerServiceForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            service = CustomerService(user=request.user, subject=subject, message=message)
            service.save()
            return redirect('customer_home')


class ViewService(DetailView):
    template_name = 'viewservice.html'
    model = CustomerService
    context_object_name = 'service'


def CheckoutView(request):
    address = Address.objects.filter(user=request.user)
    print('data :', address)
    # print(address)

    addr = []
    for i in address:
        data = {}
        # print(i.name)
        data['name'] = i.name
        data['mob'] = i.mob_no
        data['address'] = '{}, {}, {}, {}, India, {} '.format(i.house, i.street, i.town, i.state, i.pin)
        data['landmark'] = '{}'.format(i.landmark)
        data['id'] = i.id
        addr.append(data)
    print('addresses :', addr)
    context = {
        'address': addr
    }
    if request.method == "POST":
        print(request.POST)
        x = request.POST
        new_address = Address()
        new_address.user = request.user
        new_address.name = x['name']
        new_address.mob_no = x['mob_no']
        new_address.house = x['house']
        new_address.street = x['street_address']
        new_address.town = x['town']
        new_address.state = x['state']
        new_address.pin = x['pin']
        new_address.landmark = x['landmark']
        if (Address.objects.filter(house=x['house'], pin=x['pin']).exists()):
            print('already exists')
        else:
            new_address.save()
            print(new_address.street)
            return redirect("checkout")
    return render(request, 'checkout.html', context)


def summery(request, *args, **kwargs):
    Orders.objects.filter(user=request.user, status='pending').delete()
    print(kwargs.get('id'))
    print(request.user)
    cart_item = Cart.objects.filter(user=request.user, status='ordernotplaced')
    address = Address.objects.get(id=kwargs.get('id'))
    ad = '{},{},{}, {}, {}, {}, India, {} '.format(address.name, address.mob_no, address.house, address.street,
                                                   address.town, address.state, address.pin, address.landmark)
    for i in cart_item:
        print(Products.objects.get(id=i.product.id).id)
        order = Orders()
        if (Orders.objects.filter(product=Products.objects.get(id=i.product.id), user=request.user, address=ad,
                                  status='pending')).exists():
            print('already exists')
        else:
            order.product = Products.objects.get(id=i.product.id)
            order.user = request.user
            order.seller = Products.objects.get(id=i.product.id).user
            order.address = ad
            order.quantity = i.quantity
            order.save()
            print(order.date)
            print("saved")
    # address = Orders.objects.filter(user=request.user,status='pending')[0].address
    print(address)
    print("hi")
    sum = 0
    qty = 0
    data = []
    for i in cart_item:
        content = {}
        product = Products.objects.get(id=i.product_id)
        print(Products.objects.get(id=i.product_id).image.url)
        content['image'] = product.image.url
        content['name'] = product.product_name.capitalize()
        content['color'] = product.color
        content['seller'] = product.user
        content['price'] = product.price
        content['offer'] = product.offer
        content['quantity'] = i.quantity
        sum += (product.price * i.quantity)
        qty += i.quantity
        data.append(content)

    return render(request, 'order_summery.html', {'data': data, 'address': ad, 'sum': sum, 'qty': qty})


class DeleteAddress(TemplateView):
    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        address = Address.objects.get(id=id)
        address.delete()
        return redirect('checkout')


def editaddress(request, *args, **kwargs):
    id = kwargs['id']
    address = Address.objects.get(user=request.user, id=id)
    print(address.name)
    context = {'address': address}

    if request.method == "POST":
        print(request.POST)
        x = request.POST
        new_address = Address.objects.get(user=request.user, id=id)
        new_address.user = request.user
        new_address.name = x['name']
        new_address.mob_no = x['mob_no']
        new_address.house = x['house']
        new_address.street = x['street_address']
        new_address.town = x['town']
        new_address.state = x['state']
        new_address.pin = x['pin']
        new_address.landmark = x['landmark']
        if (Address.objects.filter(house=x['house'], pin=x['pin']).exists()):
            print('already exists')
        else:
            new_address.save()
            print(new_address.street)
            return redirect("checkout")
    return render(request, 'editaddress.html', context)


class GatewayView(TemplateView):
    template_name = "stripe.html"

    def get_context_data(self, **kwargs):
        cart_products = Cart.objects.filter(user=self.request.user, status='ordernotplaced')
        total = 0
        for cart in cart_products:
            total += cart.product.price * cart.quantity
        context = super().get_context_data(**kwargs)
        brands = Brand.objects.all()
        context["brands"] = brands
        context['total'] = total
        context['amount'] = total * 100
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):
    if request.method == "POST":
        charge = stripe.Charge.create(
            amount=100,
            currency="INR",
            description="Payment of product",
            source=request.POST['stripeToken']
        )
        cart_items = Cart.objects.filter(status="ordernotplaced", user=request.user)
        ordered_items = Orders.objects.filter(status="pending", user=request.user)
        for item in cart_items:
            item.status = "orderplaced"
            item.product.stock = item.product.stock - item.quantity
            item.save()
            # print(item.product.stock)
        for item in ordered_items:
            item.status = "ordered"
            item.save()
        return render(request, 'payment.html', charge)
    return render(request, 'payment.html')


def cash_on_delivery(request):
    cart_items = Cart.objects.filter(status="ordernotplaced", user=request.user)
    ordered_items = Orders.objects.filter(status="pending", user=request.user)
    for item in cart_items:
        item.status = "orderplaced"
        item.product.stock = item.product.stock - item.quantity
        item.save()
        # print(item.product.stock)
    for item in ordered_items:
        item.status = "ordered"
        item.save()
    return render(request, 'cod.html')


def view_orders(request, *args, **kwargs):
    orders = Orders.objects.filter(user=request.user)
    brands = Brand.objects.all()
    context = {
        "orders": orders,
        "brands": brands
    }
    return render(request, "vieworder.html", context)


def cancel_order(request, *args, **kwargs):
    id = kwargs.get("id")
    order = Orders.objects.get(id=id)
    order.status = "cancelled"
    order.save()
    return redirect("vieworders")
