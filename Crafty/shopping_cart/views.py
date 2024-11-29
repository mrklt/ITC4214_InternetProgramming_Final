from django.shortcuts import render

def shopping_cart(request):
    return render(request, 'shopping_cart/index.html')
