from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm, LoginForm, ProductAddForm, UpdateOrderForm, ImageForm, BrandCreationForm, \
    ProfileUserForm
from .models import Seller_Details
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView, ListView, UpdateView
from . import models
from django.contrib import messages
from customer.models import Orders
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


# Create your views here.

def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST":

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)

            profile.user = user
            profile.username = user.username
            profile.save()

            return redirect('seller_login')

        else:

            user_form = UserForm()
            profile_form = ProfileForm()

        return render(request, 'seller_registration.html', {'user_form': user_form, 'profile_form': profile_form})
    return render(request, 'seller_registration.html', {'user_form': user_form, 'profile_form': profile_form})


def LoginView(request):
    form = LoginForm()
    context = {'form': form}

    if request.method == 'POST':

        if models.Seller_Details.objects.filter(username=request.POST.get('username')).exists():
            print('user exist')

            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                # print(messages.success)
                auth.login(request, user)
                return redirect('base')
            else:

                messages.error(request, 'username or password not correct')
                # messages.error(request, 'username or password not correct')
                return redirect('seller_login')

    return render(request, 'seller_login.html', context)


def seller_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('seller_login')
    else:
        return redirect('seller_login')


def ViewProfile(request):
    detail = models.Seller_Details.objects.filter(user=request.user)

    return render(request, 'seller_profile.html', {'detail': detail})


class EditProfile(TemplateView):
    user_form = ProfileUserForm
    profile_form = ProfileForm
    template_name = "edit_profile.html"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request):
        post_data = request.POST or None
        # file_data = request.FILES or None
        try:
            details = models.Seller_Details.objects.get(user=request.user)
        except models.Seller_Details.DoesNotExist:
            details = None
        user_form = ProfileUserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, instance=details)
        # profile_form = UpdateForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse_lazy('seller_profile'))
        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        return self.render_to_response(context)


def create_brand(request):
    form = BrandCreationForm()
    context = {'form': form}
    if request.POST:
        form = BrandCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base')
    return render(request, 'create_brand.html', context)


def get_brand(id):
    return models.Brand.objects.get(id=id)


def brand_list(request):
    brands = models.Brand.objects.all()
    context = {'brands': brands}

    return render(request, 'brand_list.html', context)


def delete_brand(request, id):
    brand = get_brand(id)
    brand.delete()
    return redirect('brand_list')


def edit_brand(request, id):
    brand = get_brand(id)
    form = BrandCreationForm(instance=brand)
    context = {'form': form}
    if request.method == "POST":
        brand = get_brand(id)
        form = BrandCreationForm(instance=brand, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
        else:
            form = BrandCreationForm(request.POST)
            context = {'form': form}
            print(form.errors)
            return render(request, 'edit_brand.html', context)
    return render(request, 'edit_brand.html', context)


def add_product(request):
    form = ProductAddForm()
    image_form = ImageForm()
    context = {
        'form': form,
        'image_form': image_form
    }

    if request.method == "POST":

        form = ProductAddForm(request.POST, request.FILES)
        image_form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')
        if form.is_valid() and image_form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            for f in files:
                file_instance = models.ProductImage(images=f, product=instance)
                file_instance.save()
            return redirect('base')
        else:
            context = {
                'form': form,
                'image_form': image_form
            }

            return render(request, 'add_product.html', context)
    return render(request, 'add_product.html', context)


def product_list(request):
    s = request.user
    print(s)
    # products = models.Products.objects.all()
    products = models.Products.objects.filter(user=request.user)
    # for i in products:
    #     print(i.image.url)

    return render(request, 'seller_view_product.html', {'products': products})


def get_object(id):
    return models.Products.objects.get(id=id)


def edit_product(request, id):
    product = get_object(id)
    # images = models.ProductImage.objects.get(product=product)
    form = ProductAddForm(instance=product)
    # image_form = ImageForm(instance=product)
    context = {'form': form,
               }

    if request.method == "POST":
        form = ProductAddForm(data=request.POST, files=request.FILES, instance=product)
        # image_form = ImageForm(data=request.POST,files=request.FILES,instance=product)
        if form.is_valid():
            form.save()
            # image_form.save()
            return redirect('listallproducts')
        else:
            context = {'from': form,
                       }
            messages.error(request, "Failed to edit")
            return render(request, 'edit_product.html', context)
    return render(request, 'edit_product.html', context)


class OrderListView(ListView):
    model = Orders
    template_name = 'orderlist.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.filter(seller=self.request.user).exclude(status='cancelled')


class OrderChangeView(UpdateView):
    model = Orders
    template_name = 'orderstatus_update.html'
    form_class = UpdateOrderForm
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('orderlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        print(self.kwargs)
        order = self.model.objects.get(id=self.kwargs['id'])
        context['order'] = order
        return context


class OrderCount(TemplateView):
    template_name = 'ordercount.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        count = self.model.objects.filter(status='delivered').count()
        context['order_count'] = count
        context['orders'] = self.model.objects.filter(status='delivered')

        shipped = self.model.objects.filter(status='shipped')
        context['orders_shipped'] = shipped
        context['orders_shipped_count'] = shipped.count()

        packed = self.model.objects.filter(status='packed')
        context['orders_packed'] = packed
        context['orders_packed_count'] = packed.count()

        ordered = self.model.objects.filter(status='ordered')
        context['orders_ordered'] = ordered
        context['orders_ordered_count'] = ordered.count()

        cancelled = self.model.objects.filter(status='cancelled')
        context['orders_cancelled'] = cancelled
        context['orders_cancelled_count'] = cancelled.count()


        return context