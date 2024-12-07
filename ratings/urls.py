from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ratings'),
    path('rate/', views.rate_item, name='rate_item'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
]
