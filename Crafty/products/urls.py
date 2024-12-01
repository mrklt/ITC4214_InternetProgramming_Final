from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.product_list, name='products'),  # Changed from 'products' to 'product_list'
    path('<int:product_id>/', views.product_detail, name='product_detail'), 
]
