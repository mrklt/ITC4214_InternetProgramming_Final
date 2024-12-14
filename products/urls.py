from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.product_list, name='products'),  
    path('<int:product_id>/', views.product_detail, name='product_detail'), 
    
]
