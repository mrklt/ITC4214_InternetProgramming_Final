from django.urls import path
from . import views
from .models import Item

urlpatterns = [
    path('', views.shopping_cart, name='shopping_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/', views.product_detail, name='product_detail'), 
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
