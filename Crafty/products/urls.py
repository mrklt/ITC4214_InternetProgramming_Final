from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.products, name='products'),  # Define the 'products' URL pattern
    # Other URL patterns...
]
