from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm, LoginForm, ProductAddForm
from .models import Seller_Details
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView
from . import models
from django.contrib import messages


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

            return redirect('base')

        else:

            user_form = UserForm()
            profile_form = ProfileForm()

        return render(request, 'seller_registration.html', {'user_form': user_form, 'profile_form': profile_form})
    return render(request, 'seller_registration.html', {'user_form': user_form, 'profile_form': profile_form})


class LoginView(TemplateView):
    template_name = 'seller_login.html'
    form_class = LoginForm
    model = User

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):

        login_form = LoginForm(request.POST)

        id = User.objects.get(username=request.POST.get('username')).pk
        # print(id)
        if models.Seller_Details.objects.filter(username=request.POST.get('username')).exists():
            print('user exist')

            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('base')
            else:
                return render(request, 'seller_login.html')


def seller_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('seller_login')
    else:
        return redirect('seller_login')


def add_product(request):
    form = ProductAddForm()
    context = {}
    context['form'] = form

    if request.method == "POST":

        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # form.save()
            # print('product saved')
            messages.success(request, 'Product Added')
            return redirect('base')
        else:
            context['form'] = form
            messages.error(request, 'Failed to add')
            return render(request, 'add_product.html', context)
    return render(request, 'add_product.html', context)
