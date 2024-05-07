# views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    print('user_shop',user_shop.logo.url)
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
    print("Inside add_product view")  # Add a debug statement
    user_shop = request.user.shop  # Retrieve the shop of the current user
    print("User shop:", user_shop)  # Add a debug statement
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user_shop=user_shop)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(user_shop=user_shop)
    return render(request, 'add_product.html', {'form': form})

def add_category(request):
    print("Inside add_category view")  # Add a debug statement
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Retrieve the shop information related to the currently logged-in user
            user_shop = request.user.shop
            print("User shop:", user_shop)  # Add a debug statement
            
            # Associate the category with the shop of the currently logged-in user
            category = form.save(commit=False)
            category.shop = user_shop
            category.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


def shop_products(request):
    user_shop = get_object_or_404(Shop, user=request.user)
    products = Product.objects.filter(category__shop=user_shop)
    return render(request, 'shop_products.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get the shop of the current user
    user_shop = get_object_or_404(Shop, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user_shop=user_shop)
        if form.is_valid():
            form.save()
            return redirect('shop_products')
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = ProductForm(instance=product, user_shop=user_shop)
        
    return render(request, 'edit_product.html', {'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('shop_products')
    return render(request, 'delete_product.html', {'product': product})

def shop_orders(request):
    user_shop = get_object_or_404(Shop, user=request.user)
    orders = Order.objects.filter(shop=user_shop)  # Use 'shop' instead of 'order__shop'
    return render(request, 'shop_orders.html', {'orders': orders})

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_details.html', {'order': order})

@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        print('order_id,new_status',order_id,new_status)
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

def shop_categories(request):
    user_shop = get_object_or_404(Shop, user=request.user)
    categories = Category.objects.filter(shop=user_shop)
    return render(request, 'shop_categories.html', {'categories': categories})


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('shop_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('shop_categories')
    return render(request, 'delete_category.html', {'category': category})