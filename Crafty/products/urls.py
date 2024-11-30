from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.products, name='products'),  # Define the 'products' URL pattern
    path('<int:product_id>/', views.product_detail, name='product_detail'), 
]
