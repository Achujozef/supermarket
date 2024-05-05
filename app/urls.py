# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_shop, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
]
