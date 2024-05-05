# views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from datetime import datetime

from .forms import *
from .models import *


def register_shop(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        shop_form = ShopRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and shop_form.is_valid():
            user = user_form.save()
            shop = shop_form.save(commit=False)
            shop.user = user
            shop.save()
            login(request, user)  # Auto-login the user after registration
            return redirect('dashboard')  # Redirect to the dashboard or any other page
    else:
        user_form = UserCreationForm()
        shop_form = ShopRegistrationForm()
    return render(request, 'register_shop.html', {'user_form': user_form, 'shop_form': shop_form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def dashboard(request):
    user_shop = get_object_or_404(Shop, user=request.user)
    total_orders = Orders.objects.filter(order__shop=user_shop).count()
    total_sale = Orders.objects.filter(order__shop=user_shop).aggregate(total_sale=models.Sum('total_price'))['total_sale'] or 0
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_day = datetime.now().strftime('%A')
    total_products = Product.objects.filter(category__shop=user_shop).count()
    context = {
        'user_shop': user_shop,
        'total_orders': total_orders,
        'total_sale': total_sale,
        'today_date': today_date,
        'today_day': today_day,
        'total_products': total_products,
    }
    return render(request, 'dashboard.html', context)


def add_product(request):
    user_shop = request.user.shop  # Retrieve the shop of the current user
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user_shop=user_shop)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(user_shop=user_shop)
    return render(request, 'add_product.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Retrieve the shop information related to the currently logged-in user
            user_shop = request.user.shop
            
            # Associate the category with the shop of the currently logged-in user
            category = form.save(commit=False)
            category.shop = user_shop
            category.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})