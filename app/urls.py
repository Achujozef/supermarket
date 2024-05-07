# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_shop, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
     path('products/', views.shop_products, name='shop_products'),
    path('orders/', views.shop_orders, name='shop_orders'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('categories/', views.shop_categories, name='shop_categories'),
     path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
]
